# Generated by Django 4.0.1 on 2022-02-28 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='owner_decline',
        ),
        migrations.AddField(
            model_name='order',
            name='owner_answer',
            field=models.BooleanField(default=False, verbose_name='Owner answered on order'),
        ),
    ]
