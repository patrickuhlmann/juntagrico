# Generated by Django 4.0.1 on 2022-02-08 21:42

import datetime
import django.db.models.deletion
import django.core.validators
from django.db import migrations, models
import juntagrico.entity


class Migration(migrations.Migration):

    dependencies = [
        ('juntagrico', '0037_post_1_5'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='specialroles',
            options={'default_permissions': (), 'managed': False, 'permissions': (
                ('is_operations_group', 'Benutzer ist in der BG'), ('is_book_keeper', 'Benutzer ist Buchhalter'), ('can_send_mails', 'Benutzer kann im System E-Mails versenden'),
                ('can_use_general_email', 'Benutzer kann allgemeine E-Mail-Adresse verwenden'), ('can_use_for_members_email', 'Benutzer kann E-Mail-Adresse "for_members" verwenden'),
                ('can_use_for_subscriptions_email', 'Benutzer kann E-Mail-Adresse "for_subscription" verwenden'), ('can_use_for_shares_email', 'Benutzer kann E-Mail-Adresse "for_shares" verwenden'),
                ('can_use_technical_email', 'Benutzer kann technische E-Mail-Adresse verwenden'), ('depot_list_notification', 'Benutzer wird bei Depot-Listen-Erstellung informiert'),
                ('can_view_exports', 'Benutzer kann Exporte öffnen'), ('can_view_lists', 'Benutzer kann Listen öffnen'), ('can_generate_lists', 'Benutzer kann Listen erzeugen')
            )},
        ),
        migrations.AlterField(
            model_name='subscriptionmembership',
            name='join_date',
            field=models.DateField(blank=True, help_text='Erster Tag an dem Abo bezogen wird', null=True, verbose_name='Beitrittsdatum'),
        ),
        migrations.AlterField(
            model_name='subscriptionmembership',
            name='leave_date',
            field=models.DateField(blank=True, help_text='Letzter Tag an dem Abo bezogen wird', null=True, verbose_name='Austrittsdatum'),
        ),
        migrations.AlterField(
            model_name='subscriptionmembership',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='juntagrico.member', verbose_name='Mitglied'),
        ),
        migrations.AlterField(
            model_name='subscriptionmembership',
            name='subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='juntagrico.subscription', verbose_name='Abo'),
        ),
        migrations.AlterField(
            model_name='job',
            name='multiplier',
            field=models.FloatField(default=1.0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Arbeitseinsatz vielfaches'),
        ),
        migrations.AlterField(
            model_name='share',
            name='reason_for_acquisition',
            field=models.PositiveIntegerField(blank=True, choices=[(1, 'Gründungsmitglied'), (2, 'Beitrittserklärung'), (3, 'Beitritts- und Übertragungserklärung'), (4, 'Übertragungserklärung'),
                                                                   (5, 'Erhöhung der Anteile'), (6, 'Betriebsbeteiligung - Lohn')], null=True, verbose_name='Grund des Erwerbs'),
        ),
        migrations.AlterModelOptions(
            name='subscription',
            options={'permissions': [('can_filter_subscriptions', 'Benutzer kann Abo filtern'),
                                     ('can_change_deactivated_subscriptions', 'Benutzer kann deaktivierte Abo ändern'),
                                     ('notified_on_depot_change', 'Wird bei Depot-Änderung informiert'),
                                     ('notified_on_subscription_creation', 'Wird bei Abo Erstellung informiert'),
                                     ('notified_on_subscription_cancellation', 'Wird bei Abo Kündigung informiert')],
                     'verbose_name': 'Abo', 'verbose_name_plural': 'Abos'},
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Name')),
                ('description', models.TextField(blank=True, default='', verbose_name='Beschreibung')),
                ('visible_on_list', models.BooleanField(default=True, verbose_name='Sichtbar auf Listen')),
                ('sort_order', models.PositiveIntegerField(default=0, verbose_name='Reihenfolge')),
            ],
            options={
                'verbose_name': 'Ausfahrt',
                'verbose_name_plural': 'Ausfahrten',
                'ordering': ['sort_order'],
            },
            bases=(models.Model, juntagrico.entity.OldHolder),
        ),
        migrations.AlterUniqueTogether(
            name='delivery',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='delivery',
            name='tour',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='juntagrico.tour', verbose_name='Ausfahrt'),
        ),
        migrations.AddField(
            model_name='depot',
            name='tour',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='depots', to='juntagrico.tour', verbose_name='Ausfahrt'),
        ),
        migrations.AddConstraint(
            model_name='delivery',
            constraint=models.UniqueConstraint(fields=('delivery_date', 'tour', 'subscription_size'), name='unique_delivery'),
        ),
        migrations.AlterField(
            model_name='activityarea',
            name='description',
            field=models.TextField(default='', verbose_name='Beschreibung'),
        ),
        migrations.AlterField(
            model_name='billingperiod',
            name='code',
            field=models.TextField(blank=True, default='', verbose_name='Code für Teilabrechnung'),
        ),
        migrations.AlterField(
            model_name='depot',
            name='access_information',
            field=models.TextField(default='', help_text='Nur für Mitglieder des/r Depot sichtbar',
                                   verbose_name='Zugangsbeschreibung'),
        ),
        migrations.AlterField(
            model_name='depot',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Beschreibung'),
        ),
        migrations.AlterField(
            model_name='jobtype',
            name='description',
            field=models.TextField(default='', verbose_name='Beschreibung'),
        ),
        migrations.AlterField(
            model_name='location',
            name='description',
            field=models.TextField(blank=True, default='', verbose_name='Beschreibung'),
        ),
        migrations.AlterField(
            model_name='mailtemplate',
            name='code',
            field=models.TextField(default='', verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='mailtemplate',
            name='template',
            field=models.TextField(default='', verbose_name='Template'),
        ),
        migrations.AlterField(
            model_name='member',
            name='notes',
            field=models.TextField(blank=True, help_text='Notizen für Administration. Nicht sichtbar für Mitglied',
                                   verbose_name='Notizen'),
        ),
        migrations.AlterField(
            model_name='onetimejob',
            name='description',
            field=models.TextField(default='', verbose_name='Beschreibung'),
        ),
        migrations.AlterField(
            model_name='recuringjob',
            name='additional_description',
            field=models.TextField(blank=True, default='', verbose_name='Zusätzliche Beschreibung'),
        ),
        migrations.AlterField(
            model_name='share',
            name='notes',
            field=models.TextField(blank=True, default='',
                                   help_text='Notizen für Administration. Nicht sichtbar für Mitglied',
                                   verbose_name='Notizen'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='notes',
            field=models.TextField(blank=True, help_text='Notizen für Administration. Nicht sichtbar für Mitglied',
                                   verbose_name='Notizen'),
        ),
        migrations.AlterField(
            model_name='subscriptionproduct',
            name='description',
            field=models.TextField(blank=True, verbose_name='Beschreibung'),
        ),
        migrations.AlterField(
            model_name='subscriptionsize',
            name='description',
            field=models.TextField(blank=True, verbose_name='Beschreibung'),
        ),
        migrations.AlterField(
            model_name='subscriptiontype',
            name='description',
            field=models.TextField(blank=True, verbose_name='Beschreibung'),
        ),
        migrations.AddField(
            model_name='subscriptiontype',
            name='interval',
            field=models.PositiveIntegerField(default=1, verbose_name='Intervall'),
        ),
        migrations.AddField(
            model_name='subscriptiontype',
            name='offset',
            field=models.PositiveIntegerField(default=0, verbose_name='Versatz'),
        ),
        migrations.AlterField(
            model_name='member',
            name='end_date',
            field=models.DateField(blank=True,
                                   help_text='Voraussichtliches Datum an dem die Mitgliedschaft enden wird. Hat keinen Effekt im System',
                                   null=True, verbose_name='Enddatum'),
        ),
        migrations.AlterField(
            model_name='share',
            name='creation_date',
            field=models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Erzeugt am'),
        ),
        migrations.AlterField(
            model_name='subscriptiontype',
            name='interval',
            field=models.PositiveIntegerField(default=1,
                                              help_text='Intervall der Lieferung in Wochen,1 heisst jede Woche, 2 heisst alle 2 Wochen, usw.',
                                              validators=[django.core.validators.MinValueValidator(1)],
                                              verbose_name='Intervall'),
        ),
        migrations.AlterField(
            model_name='subscriptiontype',
            name='offset',
            field=models.PositiveIntegerField(default=0,
                                              help_text='Versatz der Lieferung in Wochen, 0 entspricht einer Lieferung ab der ersten Kalenderwoche, 1 entspricht einer Lieferung ab der zweiten Kalenderwoche, usw.',
                                              verbose_name='Versatz'),
        ),
        migrations.AlterField(
            model_name='member',
            name='iban',
            field=models.CharField(blank=True, default='', max_length=100, validators=[juntagrico.entity.validate_iban],
                                   verbose_name='IBAN'),
        ),
    ]