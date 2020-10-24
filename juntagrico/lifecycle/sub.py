from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext as _

from juntagrico.config import Config
from juntagrico.mailer import adminnotification
from juntagrico.signals import sub_activated, sub_deactivated, sub_canceled, sub_created
from juntagrico.util.lifecycle import handle_activated_deactivated, cancel_extra_sub


def sub_post_save(sender, instance, created, **kwargs):
    if created:
        sub_created.send(sender=sender, instance=instance)


def sub_pre_save(sender, instance, **kwargs):
    check_sub_consistency(instance)
    handle_activated_deactivated(instance, sender, sub_activated, sub_deactivated)
    if instance._old['cancellation_date'] is None and instance.cancellation_date is not None:
        sub_canceled.send(sender=sender, instance=instance)


def handle_sub_activated(sender, instance, **kwargs):
    instance.activation_date = instance.activation_date or timezone.now().date()
    change_date = instance.activation_date
    for part in instance.future_parts.all():
        part.activate(change_date)
    for member in instance.recipients:
        if member.subscription_current is not None:
            raise ValidationError(
                _('Ein Bezüger hat noch ein/e/n aktive/n/s {0}').format(Config.vocabulary('subscription')),
                code='invalid')
    for sub_membership in instance.subscriptionmembership_set.all():
        sub_membership.join_date = change_date
        sub_membership.save()


def handle_sub_deactivated(sender, instance, **kwargs):
    instance.deactivation_date = instance.deactivation_date or timezone.now().date()
    change_date = instance.deactivation_date
    for extra in instance.extra_subscription_set.all():
        extra.deactivate(change_date)
    for part in instance.active_parts.all():
        part.deactivate(change_date)
    for part in instance.future_parts.all():
        part.delete()
    for sub_membership in instance.subscriptionmembership_set.all():
        sub_membership.member.leave_subscription(instance)


def handle_sub_canceled(sender, instance, **kwargs):
    instance.cancellation_date = instance.cancellation_date or timezone.now().date()
    for extra in instance.extra_subscription_set.all():
        cancel_extra_sub(extra)
    for part in instance.active_parts.all():
        part.cancel()
    for part in instance.future_parts.all():
        part.delete()


def handle_sub_created(sender, instance, **kwargs):
    adminnotification.subscription_created(instance)


def check_sub_consistency(instance):
    if instance._old['deactivation_date'] is not None and instance.deactivation_date is None:
        raise ValidationError(
            _('Deaktivierte {0} koennen nicht wieder aktiviert werden').format(Config.vocabulary('subscription_pl')),
            code='invalid')
    pm_sub = instance.primary_member in instance.recipients
    pm_form = instance._future_members and instance.primary_member in instance._future_members
    if instance.primary_member is not None and not (pm_sub or pm_form):
        raise ValidationError(
            _('HauptbezieherIn muss auch {}-BezieherIn sein').format(Config.vocabulary('subscription')),
            code='invalid')
