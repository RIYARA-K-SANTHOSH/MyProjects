# Generated by Django 5.0.6 on 2024-08-26 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimonyapp', '0048_register_blocked'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='complexion',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
