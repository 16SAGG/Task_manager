# Generated by Django 4.0.4 on 2022-12-19 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0008_alter_task_deadline_alter_task_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completionDate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='creationDate',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(blank=True, choices=[('Medium', 'Medium'), ('low', 'low'), ('High', 'High')], max_length=32, null=True),
        ),
    ]
