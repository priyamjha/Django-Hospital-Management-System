# Generated by Django 5.1 on 2024-08-23 16:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MediAccess', '0009_alter_customuser_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientrecord',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='MediAccess.department'),
        ),
    ]
