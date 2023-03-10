# Generated by Django 4.1.4 on 2022-12-17 21:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('creationDate', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('description', models.TextField(blank=True, max_length=255)),
                ('creationDate', models.DateTimeField(auto_now_add=True)),
                ('completionDate', models.DateTimeField(null=True)),
                ('deadline', models.DateTimeField(null=True)),
                ('priority', models.CharField(blank=True, choices=[('low', 'low'), ('Medium', 'Medium'), ('High', 'High')], max_length=32, null=True)),
                ('categories', models.ManyToManyField(blank=True, null=True, to='task.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
