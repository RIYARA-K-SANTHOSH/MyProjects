# Generated by Django 5.0.6 on 2024-08-10 17:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimonyapp', '0034_blog_membershipplan_notification'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalInfo',
            fields=[
                ('personal_id', models.AutoField(primary_key=True, serialize=False)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('marital_status', models.CharField(blank=True, choices=[('single', 'Single'), ('divorced', 'Divorced'), ('widowed', 'Widowed')], max_length=20, null=True)),
                ('height', models.CharField(blank=True, max_length=10, null=True)),
                ('weight', models.CharField(blank=True, max_length=10, null=True)),
                ('blood_group', models.CharField(blank=True, max_length=10, null=True)),
                ('hobbies', models.TextField(blank=True, null=True)),
                ('occupation', models.CharField(blank=True, max_length=100, null=True)),
                ('annual_income', models.CharField(blank=True, max_length=20, null=True)),
                ('about_me', models.TextField(blank=True, null=True)),
                ('reg_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='personal_info', to='matrimonyapp.register')),
            ],
        ),
    ]