# Generated by Django 5.0.6 on 2024-08-25 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimonyapp', '0047_alter_family_reg_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='blocked',
            field=models.BooleanField(default=False),
        ),
    ]
