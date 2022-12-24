from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm, StatusForm
from .models import Task, Status
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone


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
def createTasks(request, choiceStatId):
    priorityChoices = Task.priorityChoices
    status = Status.objects.filter(user = request.user)
    minDate = timezone.now()
    formatMinDate = minDate.strftime("%Y-%m-%d")
    if request.method == 'GET':
        ctxt = {
            'choiceStatId': choiceStatId,
            'myStatus': status,
            'priorityChoices': priorityChoices,
            'formatMinDate' : formatMinDate,
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
                'choiceStatId': choiceStatId,
                'myStatus': status,
                'priorityChoices': priorityChoices,
                'formatMinDate' : formatMinDate,
                'advice': 'Title and deadline are required.',
            }
            return render(request, 'create_tasks.html', ctxt)

@login_required
def taskDetail(request, taskId):
    if request.method == 'GET':
        priorityChoices = Task.priorityChoices
        status = Status.objects.filter(user = request.user)
        myTask = get_object_or_404(Task, pk = taskId, user = request.user)
        minDate = timezone.now()
        formatMinDate = minDate.strftime("%Y-%m-%d")
        deadline = myTask.deadline
        formatDeadline = deadline.strftime("%Y-%m-%d")
        ctxt = {
            'myTask': myTask,
            'myStatus': status,
            'taskDetail': True,
            'priorityChoices': priorityChoices,
            'formatDeadline' : formatDeadline,
            'formatMinDate' : formatMinDate,
        }
        return render(request, 'create_tasks.html', ctxt)
    else:
        try:
            myTask = get_object_or_404(Task, pk = taskId, user = request.user)
            form = TaskForm(request.POST, instance = myTask)
            form.save()
            return redirect('tasks')
        except ValueError:
            priorityChoices = Task.priorityChoices
            status = Status.objects.filter(user = request.user)
            myTask = get_object_or_404(Task, pk = taskId, user = request.user)
            minDate = timezone.now()
            formatMinDate = minDate.strftime("%Y-%m-%d")
            deadline = myTask.deadline
            formatDeadline = deadline.strftime("%Y-%m-%d")
            ctxt = {
                'myTask': myTask,
                'myStatus': status,
                'taskDetail': True,
                'priorityChoices': priorityChoices,
                'advice': 'Title and deadline are required.',
                'formatDeadline' : formatDeadline,
                'formatMinDate' : formatMinDate,
            }
            return render(request, 'create_tasks.html', ctxt)

@login_required
def taskDeleted(request, taskId):
    myTask = get_object_or_404(Task, pk = taskId, user = request.user)
    myTask.delete()
    return redirect('tasks')

@login_required
def createStatus(request):
    if request.method == 'GET':
        return render(request, 'create_status.html', {})
    else:
        try:
            form = StatusForm(request.POST)
            newStatus = form.save(commit = False)
            newStatus.user = request.user
            newStatus.save()
            return redirect('tasks')
        except ValueError:
            ctxt = {
                'advice': "Error creating status",
            }
            return render(request, 'create_status.html', ctxt)

@login_required
def statusDetail(request, statusId):
    if request.method == 'GET':
        myStatus = get_object_or_404(Status, pk = statusId, user = request.user)
        ctxt = {
            'myStatus': myStatus,
            'statusDetail': True,
        }
        return render(request, 'create_status.html', ctxt)
    else:
        try:
            myStatus = get_object_or_404(Status, pk = statusId, user = request.user)
            form = StatusForm(request.POST, instance = myStatus)
            form.save()
            return redirect('tasks')
        except ValueError:
            myStatus = get_object_or_404(Status, pk = statusId, user = request.user)
            ctxt = {
                'myStatus': myStatus,
                'statusDetail': True,
                'advice': 'Error updating status',
            }
            return render(request, 'create_status.html', ctxt)

@login_required
def statusDeleted(request, statusId):
    myStatus = get_object_or_404(Status, pk = statusId, user = request.user)
    myStatus.delete()
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
        return render(request, 'signup.html', {})
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
                    'advice': "User already exists."
                }
                return render(request, 'signup.html', ctxt)
        else:
            if request.POST['username'] == '':
                ctxt = {
                    'advice': "Username cant'be a void value."
                }
            elif len(request.POST['password1']) < minPasswordSize:
                ctxt = {
                    'advice': "Use at least eigth characters in the password."
                }
            elif request.POST['password1'] != request.POST['password2']:
                ctxt = {
                    'advice': "Password don't match."
                }
            return render(request, 'signup.html', ctxt)

