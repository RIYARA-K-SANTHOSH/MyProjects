# Generated by Django 5.0.6 on 2024-10-17 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matrimonyapp', '0059_alter_payment_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='user',
            new_name='reg_id',
        ),
    ]
