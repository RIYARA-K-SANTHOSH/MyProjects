# Generated by Django 5.0.6 on 2024-08-10 13:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimonyapp', '0030_delete_blog_remove_education_reg_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('login_id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=128)),
                ('reg_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logins', to='matrimonyapp.register')),
            ],
        ),
    ]