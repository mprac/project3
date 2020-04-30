# Generated by Django 2.0.3 on 2020-04-30 04:26

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(blank=True, max_length=64)),
                ('city', models.CharField(blank=True, max_length=64)),
                ('state', models.CharField(blank=True, max_length=2)),
                ('zipcode', models.IntegerField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name=datetime.datetime(2020, 4, 30, 4, 26, 44, 982514, tzinfo=utc))),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='menuItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.Item')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(choices=[('PU', 'Pick up'), ('DL', 'Delivery')], default='PU', max_length=64)),
                ('count', models.IntegerField()),
                ('status', models.CharField(choices=[('CRT', 'In Cart'), ('PLCD', 'Placed'), ('CKNG', 'Cooking'), ('OFD', 'Out For Delivery'), ('RDY', 'Ready For Pickup'), ('CMP', 'Order Complete')], default='CRT', max_length=64)),
                ('instructions', models.TextField(blank=True, max_length=300)),
                ('address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.Address')),
                ('menuItem', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.menuItem')),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='orders.Menu')),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='price',
            name='Topping',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='orders.Topping'),
        ),
        migrations.AddField(
            model_name='order',
            name='toppings',
            field=models.ManyToManyField(blank=True, to='orders.Topping'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='orders.Section'),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='size',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='sizes', to='orders.Size'),
        ),
        migrations.AddField(
            model_name='menuitem',
            name='style',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='styles', to='orders.Style'),
        ),
        migrations.AddField(
            model_name='cart',
            name='orders',
            field=models.ManyToManyField(to='orders.Order'),
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL),
        ),
    ]
