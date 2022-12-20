from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.shortcuts import get_object_or_404

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

def tasks(request):
    toDoTasks = Task.objects.filter(user = request.user, completionDate__isnull = True)
    ctxt = {
        'toDoTasks': toDoTasks,
    }
    return render(request, 'tasks.html', ctxt)

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

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        ctxt = {
            'form': AuthenticationForm,
        }
        return render(request, 'signin.html', ctxt)
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            ctxt = {
            'form': AuthenticationForm,
            'advice': 'User or password is incorrect',
            }
            return render(request, 'signin.html', ctxt)
        else:
            login(request, user)
            return redirect('tasks')
