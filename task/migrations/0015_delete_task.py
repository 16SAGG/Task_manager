# Generated by Django 4.0.4 on 2022-12-19 23:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0014_task_deadline_alter_task_priority'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Task',
        ),
    ]
