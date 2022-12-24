from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task, Status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html', {})

@login_required
def tasks(request):
    tasks = Task.objects.filter(user = request.user)
    status = Status.objects.filter(user = request.user)
    ctxt = {
        'myTasks': tasks,
        'myStatus': status,
    }
    return render(request, 'tasks_list.html', ctxt)

@login_required
def createTasks(request):
    deadlineChoices = Task.deadlineChoices
    priorityChoices = Task.priorityChoices
    status = Status.objects.filter(user = request.user)
    if request.method == 'GET':
        ctxt = {
            'myStatus': status,
            'deadlineChoices': deadlineChoices,
            'priorityChoices': priorityChoices,
        }
        return render(request, 'create_tasks.html', ctxt)
    else:
        try:
            form = TaskForm(request.POST)
            newTask = form.save(commit = False)
            newTask.user = request.user
            newTask.save()
            return redirect('tasks')
        except ValueError:
            ctxt = {
                'myStatus': status,
                'advice': 'Please provide valid data'
            }
            return render(request, 'create_tasks.html', ctxt)

@login_required
def taskDetail(request, taskId):
    if request.method == 'GET':
        deadlineChoices = Task.deadlineChoices
        priorityChoices = Task.priorityChoices
        status = Status.objects.filter(user = request.user)
        myTask = get_object_or_404(Task, pk = taskId, user = request.user)
        ctxt = {
            'myTask': myTask,
            'myStatus': status,
            'taskDetail': True,
            'deadlineChoices': deadlineChoices,
            'priorityChoices': priorityChoices,
        }
        return render(request, 'create_tasks.html', ctxt)
    else:
        try:
            myTask = get_object_or_404(Task, pk = taskId, user = request.user)
            form = TaskForm(request.POST, instance = myTask)
            form.save()
            return redirect('tasks')
        except ValueError:
            deadlineChoices = Task.deadlineChoices
            priorityChoices = Task.priorityChoices
            status = Status.objects.filter(user = request.user)
            myTask = get_object_or_404(Task, pk = taskId, user = request.user)
            ctxt = {
                'myTask': myTask,
                'myStatus': status,
                'taskDetail': True,
                'deadlineChoices': deadlineChoices,
                'priorityChoices': priorityChoices,
                'Advice': 'Error updating task.'
            }
            return render(request, 'create_tasks.html', ctxt)

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

def signup(request):
    if request.method == 'GET':
        ctxt = {
            'form': UserCreationForm,
        }
        return render(request, 'signup.html', ctxt)
    else:
        minPasswordSize = 8
        if request.POST['username'] and len(request.POST['password1']) >= minPasswordSize and request.POST['password1'] == request.POST['password2']:
            try:
                newUser = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                newUser.save()
                login(request, newUser)
                return redirect('tasks')
            except IntegrityError:
                ctxt = {
                    'form': UserCreationForm,
                    'advice': "User already exists."
                }
                return render(request, 'signup.html', ctxt)
        else:
            if request.POST['username'] == '':
                ctxt = {
                        'form': UserCreationForm,
                        'advice': "Username cant'be a void value."
                }
            elif len(request.POST['password1']) < minPasswordSize:
                ctxt = {
                        'form': UserCreationForm,
                        'advice': "Use at least eigth characters in the password."
                }
            elif request.POST['password1'] != request.POST['password2']:
                ctxt = {
                        'form': UserCreationForm,
                        'advice': "Password don't match."
                }
            return render(request, 'signup.html', ctxt)

