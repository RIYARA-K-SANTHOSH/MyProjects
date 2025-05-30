# Generated by Django 5.0.6 on 2024-08-08 17:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimonyapp', '0018_remove_register_confirm_password_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FamilyDetails',
            fields=[
                ('familydetail_id', models.AutoField(primary_key=True, serialize=False)),
                ('father_name', models.CharField(max_length=100)),
                ('father_occupation', models.CharField(blank=True, max_length=100, null=True)),
                ('mother_name', models.CharField(max_length=100)),
                ('mother_occupation', models.CharField(blank=True, max_length=100, null=True)),
                ('sibling_count', models.IntegerField(blank=True, null=True)),
                ('sibling_details', models.TextField(blank=True, null=True)),
                ('family_type', models.CharField(choices=[('Joint', 'Joint'), ('Nuclear', 'Nuclear'), ('Extended', 'Extended')], max_length=10)),
                ('family_status', models.CharField(choices=[('Middle Class', 'Middle Class'), ('Upper Middle Class', 'Upper Middle Class'), ('Rich', 'Rich')], max_length=20)),
                ('family_values', models.CharField(choices=[('Traditional', 'Traditional'), ('Moderate', 'Moderate'), ('Liberal', 'Liberal')], max_length=20)),
                ('nativeplace', models.CharField(blank=True, max_length=100, null=True)),
                ('reg_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
