# Generated by Django 5.1.1 on 2025-04-04 13:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_bankaccount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bankaccount',
            name='message',
        ),
    ]
