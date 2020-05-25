# Generated by Django 3.0.6 on 2020-05-20 18:56

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0016_auto_20200517_0316'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='toppingCount',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2020, 5, 20, 18, 56, 19, 963899, tzinfo=utc)),
        ),
    ]