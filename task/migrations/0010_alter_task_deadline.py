# Generated by Django 4.0.4 on 2022-12-19 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0009_alter_task_completiondate_alter_task_creationdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.IntegerField(blank=True, choices=[(32, '(32) Thirty two weeks'), (20, '(20) Twenty weeks'), (12, '(12) Twelve weeks'), (48, '(48) Fourty eight weeks'), (8, '(8) Eight weeks'), (16, '(16) Sixteen weeks'), (24, '(24) Twenty four weeks'), (2, '(2) Two weeks'), (36, '(36) Thirty six weeks'), (28, '(28) Tweny eight weeks'), (3, '(3) Three weeks'), (4, '(4) Four weeks'), (40, '(40) Fourty weeks'), (1, '(1) One week'), (44, '(44) Fourty four weeks')], null=True),
        ),
    ]
