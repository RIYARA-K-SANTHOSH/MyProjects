# Generated by Django 5.0.6 on 2024-08-08 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimonyapp', '0020_register_confirm_password_alter_register_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='password',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='register',
            name='reset_password_token',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
