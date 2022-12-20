from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html', {})

def signup(request):
    if request.method == 'GET':
        ctxt = {
            'form': UserCreationForm,
        }
        return render(request, 'signup.html', ctxt)
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                newUser = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                newUser.save()
                login(request, newUser)
                return redirect('tasks')
            except IntegrityError:
                ctxt = {
                    'form': UserCreationForm,
                    'advice': "User already exists"
                }
                return render(request, 'signup.html', ctxt)
        else:
            ctxt = {
                    'form': UserCreationForm,
                    'advice': "Password don't match"
            }
            return render(request, 'signup.html', ctxt)

@login_required
def tasks(request):
    toDoTasks = Task.objects.filter(user = request.user, completionDate__isnull = True)
    doneTasks = Task.objects.filter(user = request.user, completionDate__isnull = False).order_by('-completionDate')
    ctxt = {
        'toDoTasks': toDoTasks,
        'doneTasks': doneTasks,
    }
    return render(request, 'tasks.html', ctxt)

@login_required
def createTasks(request):
    if request.method == 'GET':
        ctxt = {
            'form': TaskForm
        }
        return render(request, 'create_tasks.html', ctxt)
    else:
        try:
            form = TaskForm(request.POST)
            newTask = form.save(commit = False)
            newTask.user = request.user
            newTask.save()
            ctxt = {
                'form': TaskForm,
                'advice': 'Task has been created successfully'
            }
            return render(request, 'create_tasks.html', ctxt)
        except ValueError:
            ctxt = {
                'form': TaskForm,
                'advice': 'Please provide valid data'
            }
            return render(request, 'create_tasks.html', ctxt)

@login_required
def taskDetail(request, taskId):
    if request.method == 'GET':
        myTask = get_object_or_404(Task, pk = taskId, user = request.user)
        form = TaskForm(instance = myTask)
        ctxt = {
            'myTask': myTask,
            'form': form,
        }
        return render(request, 'task_detail.html', ctxt)
    else:
        try:
            myTask = get_object_or_404(Task, pk = taskId, user = request.user)
            form = TaskForm(request.POST, instance = myTask)
            form.save()
            return redirect('tasks')
        except ValueError:
            ctxt = {
                'myTask': myTask,
                'form': form,
                'advice': 'Error updating task',
            }
            return render(request, 'task_detail.html', ctxt)

@login_required
def taskCompleted(request, taskId):
    if request.method == 'POST':
        myTask = get_object_or_404(Task, pk = taskId, user = request.user)
        myTask.completionDate = timezone.now()
        myTask.save()
        return redirect('tasks')

@login_required
def taskUncomplete(request, taskId):
    if request.method == 'POST':
        myTask = get_object_or_404(Task, pk = taskId, user = request.user)
        myTask.completionDate = None
        myTask.save()
        return redirect('tasks')

@login_required
def taskDeleted(request, taskId):
    if request.method == 'POST':
        myTask = get_object_or_404(Task, pk = taskId, user = request.user)
        myTask.delete()
        return redirect('tasks')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            ctxt = {
            'advice': 'User or password is incorrect',
            }
            return render(request, 'signin.html', ctxt)
        else:
            login(request, user)
            return redirect('tasks')
