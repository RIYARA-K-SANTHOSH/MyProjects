# Generated by Django 5.0.6 on 2024-08-08 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimonyapp', '0019_familydetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='confirm_password',
            field=models.CharField(default=1, max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='register',
            name='first_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='register',
            name='last_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='register',
            name='location',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='register',
            name='reset_password_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]