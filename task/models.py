import datetime
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone, dateformat

class Status(models.Model):
    title = models.CharField(max_length = 32)
    creationDate = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status'
    
    def __str__(self) -> str:
        return self.title

class Task(models.Model):
    title = models.CharField(max_length = 34)
    description = models.TextField(max_length = 1080, blank = True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    creationDate = models.DateField(auto_now_add = True)
    completionDate = models.DateField(blank = True, null = True)
    deadline = models.DateField( null=True)
    priorityChoices = (
        ('low', 'low'),
        ('medium', 'medium'),
        ('high', 'high'),
    )
    priority = models.CharField(max_length = 32, blank = True, null = True, choices = priorityChoices)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
    
    def __str__(self) -> str:
        return self.title
    