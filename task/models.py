import datetime
from django.db import models
from django.contrib.auth.models import User

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
    title = models.CharField(max_length = 32)
    description = models.TextField(max_length = 255, blank = True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    creationDate = models.DateField(auto_now_add = True)
    completionDate = models.DateField(blank = True, null = True)
    deadlineChoices = (
        (1, '(1) One week'),
        (2, '(2) Two weeks'),
        (3, '(3) Three weeks'),
        (4, '(4) Four weeks'),
        (8, '(8) Eight weeks'),
        (12, '(12) Twelve weeks'),
        (16, '(16) Sixteen weeks'),
        (20, '(20) Twenty weeks'),
        (24, '(24) Twenty four weeks'),
        (28, '(28) Tweny eigth weeks'),
        (32, '(32) Thirty two weeks'),
        (36, '(36) Thirty six weeks'),
        (40, '(40) Fourty weeks'),
        (44, '(44) Fourty four weeks'),
        (48, '(48) Fourty eigth weeks'),
    )
    deadline = models.IntegerField(blank = True, null = True, choices = deadlineChoices)
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
    