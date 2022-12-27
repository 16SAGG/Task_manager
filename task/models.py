from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.core.exceptions import ValidationError

class Board(models.Model):
    title = models.CharField(max_length = 34)
    creationDate = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Board'
        verbose_name_plural = 'Boards'
    
    def __str__(self) -> str:
        return self.title + " - " + self.user.username

class Status(models.Model):
    title = models.CharField(max_length = 34)
    creationDate = models.DateTimeField(auto_now_add = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    board = models.ForeignKey(Board, on_delete = models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status'
    
    def __str__(self) -> str:
        return self.title + " - " + self.board.title + " - " + self.user.username

class Task(models.Model):
    title = models.CharField(max_length = 34)
    description = models.TextField(max_length = 1080, blank = True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, null=True)
    creationDate = models.DateField(auto_now_add = True)
    deadline = models.DateField(blank=True, null = True)
    priorityChoices = (
        ('low', 'low'),
        ('medium', 'medium'),
        ('high', 'high'),
    )
    priority = models.CharField(max_length = 32, blank = True, null = True, choices = priorityChoices)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def clean(self, *args, **kwargs):
        super(Task, self).clean(*args, **kwargs)
        if self.deadline:
            if self.deadline <= datetime.now().date():
                raise ValueError('Deadline must be later than now.')
    
    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
    
    def __str__(self) -> str:
        return self.title + " - " + self.status.title + " - " + self.status.board.title + " - " + self.user.username
    