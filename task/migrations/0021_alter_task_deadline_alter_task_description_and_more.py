# Generated by Django 4.0.4 on 2022-12-24 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0020_status_user_alter_task_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, max_length=1080),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.CharField(blank=True, choices=[('low', 'low'), ('medium', 'medium'), ('high', 'high')], max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=34),
        ),
    ]
