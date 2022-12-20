# Generated by Django 4.1.4 on 2022-12-17 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_alter_task_options_alter_task_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completionDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(blank=True, choices=[('low', 'low'), ('High', 'High'), ('Medium', 'Medium')], max_length=32, null=True),
        ),
    ]
