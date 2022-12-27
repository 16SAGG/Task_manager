from django.forms import ModelForm
from .models import Task, Status, Board

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'status', 'deadline', 'priority',)

class StatusForm(ModelForm):
    class Meta:
        model = Status
        fields = ('title', 'board',)

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ('title',)