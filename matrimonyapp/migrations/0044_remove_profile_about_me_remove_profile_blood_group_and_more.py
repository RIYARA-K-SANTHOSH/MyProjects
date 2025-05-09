# Generated by Django 5.0.6 on 2024-08-22 15:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimonyapp', '0043_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='about_me',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='blood_group',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='location',
        ),
        migrations.AddField(
            model_name='profile',
            name='about',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='caste',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='more_about_me',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='physical_status',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='spoken_language',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='profile',
            name='annual_income',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='height',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='hobbies',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='marital_status',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mother_tongue',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='occupation',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='reg_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='matrimonyapp.register'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='religion',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='profile',
            name='weight',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
