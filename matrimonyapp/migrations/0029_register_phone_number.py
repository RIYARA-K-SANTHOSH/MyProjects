# Generated by Django 5.0.6 on 2024-08-10 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimonyapp', '0028_remove_notification_reg_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='phone_number',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
    ]
