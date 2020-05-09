# Generated by Django 2.0.3 on 2020-05-07 03:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2020, 5, 7, 3, 34, 40, 492609, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='topping',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=4),
            preserve_default=False,
        ),
    ]