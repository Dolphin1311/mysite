# Generated by Django 4.0.1 on 2022-01-20 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0002_advertisingspace_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AdvertisingSpaceType',
            new_name='AdvertisingSpaceCategory',
        ),
        migrations.RenameField(
            model_name='advertisingspace',
            old_name='advertising_space_type',
            new_name='advertising_space_category',
        ),
    ]
