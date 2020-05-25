# Generated by Django 2.0.3 on 2020-05-09 22:43

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20200509_2224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sizeprice',
            name='menuitem_ptr',
        ),
        migrations.RemoveField(
            model_name='sizeprice',
            name='size',
        ),
        migrations.AddField(
            model_name='menuitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=4),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='menuitem',
            name='size',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='orders.Size'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cart',
            name='date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2020, 5, 9, 22, 42, 56, 962011, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menuitems', to='orders.Item'),
        ),
        migrations.DeleteModel(
            name='sizePrice',
        ),
    ]