# Generated by Django 5.1.1 on 2024-10-27 04:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizzashopapp', '0008_alter_order_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.AddField(
            model_name='customer',
            name='orders',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pizzashopapp.order'),
        ),
    ]