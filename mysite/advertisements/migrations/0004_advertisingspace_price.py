# Generated by Django 4.0.1 on 2022-01-20 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0003_rename_advertisingspacetype_advertisingspacecategory_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisingspace',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8),
        ),
    ]
