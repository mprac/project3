# Generated by Django 2.0.3 on 2020-05-05 03:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20200505_0317'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='hasToppings',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2020, 5, 5, 3, 29, 21, 149892, tzinfo=utc)),
        ),
    ]
