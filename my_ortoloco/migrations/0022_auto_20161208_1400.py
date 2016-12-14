# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-08 13:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    def data_migration(apps, schema_editor):
        Abo = apps.get_model("my_ortoloco", "Abo")
        Anteilschein = apps.get_model("my_ortoloco", "Anteilschein")
        ExtraAbo = apps.get_model("my_ortoloco", "ExtraAbo")
        Billable = apps.get_model("my_ortoloco", "Billable")
        Loco = apps.get_model("my_ortoloco", "Loco")
        
        ContentType = apps.get_model("contenttypes", "ContentType")
        
        abo_ct = ContentType.objects.filter(model='abo')[0]
        for abo in Abo.objects.all():
            billable = Billable.objects.create()
            billable.polymorphic_ctype_id = abo_ct.id
            billable.save()
            billable.refresh_from_db()
            abo.billable_ptr=billable.id
            for loco in abo.locos.all():
                loco.tmp_abo_id=billable.id
                loco.save() 
            for extra in abo.extra_abo_set.all():
                extra.tmp_abo_id=billable.id
                extra.save()
            abo.save()  
                
        share_ct = ContentType.objects.filter(model='anteilschein')[0]
        for share in Anteilschein.objects.all():
            billable = Billable.objects.create()
            billable.polymorphic_ctype_id = share_ct.id
            billable.save()
            billable.refresh_from_db()
            share.billable_ptr=billable.id
            share.save()    
                     
        extra_ct = ContentType.objects.filter(model='extraabo')[0]
        for extra in ExtraAbo.objects.all():
            billable = Billable.objects.create()
            billable.polymorphic_ctype_id = extra_ct.id
            billable.save()
            billable.refresh_from_db()
            extra.billable_ptr=billable.id
            extra.save()
                       

    dependencies = [
        ('my_ortoloco', '0021_auto_20161114_1248'),
    ]

    operations = [
        migrations.RunPython(data_migration),
    ]