# Generated by Django 4.0.1 on 2022-02-08 21:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('juntagrico', '0037_post_1_5'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='specialroles',
            options={'default_permissions': (), 'managed': False, 'permissions': (('is_operations_group', 'Benutzer ist in der BG'), ('is_book_keeper', 'Benutzer ist Buchhalter'), ('can_send_mails', 'Benutzer kann im System E-Mails versenden'), ('can_use_general_email', 'Benutzer kann allgemeine E-Mail-Adresse verwenden'), ('can_use_for_members_email', 'Benutzer kann E-Mail-Adresse "for_members" verwenden'), ('can_use_for_subscriptions_email', 'Benutzer kann E-Mail-Adresse "for_subscription" verwenden'), ('can_use_for_shares_email', 'Benutzer kann E-Mail-Adresse "for_shares" verwenden'), ('can_use_technical_email', 'Benutzer kann technische E-Mail-Adresse verwenden'), ('depot_list_notification', 'Benutzer wird bei Depot-Listen-Erstellung informiert'), ('can_view_exports', 'Benutzer kann Exporte öffnen'), ('can_view_lists', 'Benutzer kann Listen öffnen'))},
        ),
    ]
