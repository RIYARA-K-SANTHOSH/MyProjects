# Generated by Django 5.0.6 on 2024-08-10 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matrimonyapp', '0027_remove_notification_user_notification_reg_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='reg_id',
        ),
    ]