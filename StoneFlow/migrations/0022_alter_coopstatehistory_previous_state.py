# Generated by Django 5.1.1 on 2025-07-06 21:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StoneFlow', '0021_alter_coopstatehistory_previous_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coopstatehistory',
            name='previous_state',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prev_history', to='StoneFlow.step'),
        ),
    ]
