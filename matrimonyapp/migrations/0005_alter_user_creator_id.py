# Generated by Django 5.0.6 on 2024-07-09 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimonyapp', '0004_login'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='creator_id',
            field=models.IntegerField(unique=True),
        ),
    ]
