# Generated by Django 5.0.6 on 2024-08-10 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimonyapp', '0032_register_last_login_register_token_expiry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='register',
            name='confirm_password',
        ),
        migrations.RemoveField(
            model_name='register',
            name='last_login',
        ),
        migrations.AddField(
            model_name='register',
            name='reset_password_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
