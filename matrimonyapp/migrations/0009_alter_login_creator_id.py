# Generated by Django 5.0.6 on 2024-07-31 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimonyapp', '0008_user_last_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='creator_id',
            field=models.CharField(max_length=100),
        ),
    ]
