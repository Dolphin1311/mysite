# Generated by Django 4.0.1 on 2022-03-03 14:08

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('advertisements', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('is_confirmed', models.BooleanField(default=False, verbose_name='Is confirmed')),
                ('owner_answer', models.BooleanField(default=False, verbose_name='Owner answered on order')),
                ('date_from', models.DateField(default=django.utils.timezone.now, verbose_name='Date from')),
                ('date_to', models.DateField(default=django.utils.timezone.now, verbose_name='Date to')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('advertising_space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advertisements.advertisingspace', verbose_name='Advertising space id')),
            ],
        ),
    ]
