# Generated by Django 5.0.6 on 2024-09-20 04:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimonyapp', '0051_delete_membershipplan'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/images/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('reg_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='matrimonyapp.register')),
            ],
        ),
    ]
