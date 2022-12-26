from django.contrib import admin
from .models import Status , Task, Board

# Register your models here.
admin.site.register(Task)
admin.site.register(Status)
admin.site.register(Board)

