# Generated by Django 2.0.3 on 2020-05-09 20:07

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20200509_0152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menuitem',
            name='price',
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='size',
        ),
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2020, 5, 9, 20, 7, 23, 244276, tzinfo=utc)),
        ),
    ]