# Generated by Django 5.0.6 on 2024-08-09 16:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimonyapp', '0021_alter_login_password_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='education',
            name='college_details',
        ),
        migrations.RemoveField(
            model_name='education',
            name='school_details',
        ),
        migrations.RemoveField(
            model_name='education',
            name='university_details',
        ),
        migrations.AddField(
            model_name='register',
            name='is_blocked',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='education',
            name='reg_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='matrimonyapp.register'),
        ),
        migrations.AlterField(
            model_name='login',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]