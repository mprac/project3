# Generated by Django 2.0.3 on 2020-05-09 20:08

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20200509_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2020, 5, 9, 20, 8, 19, 97156, tzinfo=utc)),
        ),
    ]