# Generated by Django 5.0.6 on 2024-07-09 13:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimonyapp', '0005_alter_user_creator_id'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalInfo',
            fields=[
                ('additional_id', models.AutoField(primary_key=True, serialize=False)),
                ('dob', models.DateField(blank=True, null=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('height', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('hobbies', models.CharField(blank=True, max_length=255, null=True)),
                ('skills', models.CharField(blank=True, max_length=255, null=True)),
                ('interests', models.CharField(blank=True, max_length=255, null=True)),
                ('more_details', models.TextField(blank=True, null=True)),
                ('job_title', models.CharField(blank=True, max_length=100, null=True)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]