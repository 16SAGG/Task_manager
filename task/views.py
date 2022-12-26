from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm, StatusForm
from .models import Task, Status, Board
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime
from django.conf import settings


def home(request):
    if request.user.is_authenticated:
        boards = Board.objects.filter(user = request.user)
        ctxt = {
            'myBoards' :  boards,
        }
        return render(request, 'home_authenticated.html', ctxt)
    else:   
        return render(request, 'home.html', {})

@login_required
def tasks(request, boardId):
    myBoard = get_object_or_404(Board, pk = boardId, user = request.user)
    tasks = Task.objects.filter(user = request.user)
    status = Status.objects.filter(user = request.user)
    ctxt = {
        'myTasks': tasks,
        'myStatus': status,
        'myBoard' : myBoard,
    }
    return render(request, 'tasks_list.html', ctxt)

@login_required
def createTasks(request, choiceStatId, boardId):
    priorityChoices = Task.priorityChoices
    myBoard = get_object_or_404(Board, pk = boardId, user = request.user)
    status = Status.objects.filter(user = request.user)
    minDate = timezone.now()
    formatMinDate = minDate.strftime("%Y-%m-%d")
    ctxt = {
        'choiceStatId': choiceStatId,
        'myStatus': status,
        'priorityChoices': priorityChoices,
        'formatMinDate' : formatMinDate,
        'myBoard' : myBoard, 
    }
    if request.method == 'POST':
        try:
            form = TaskForm(request.POST)
            newTask = form.save(commit = False)
            newTask.user = request.user
            newTask.save()
            return redirect('tasks', boardId = boardId)
        except ValueError:
            maxTitleSize = settings.GLOBAL_SETTINGS['TITLE_TEXT_INPUT']
            maxDescriptionSize = settings.GLOBAL_SETTINGS['AREA_TEXT_INPUT']
            if len(request.POST['title']) == 0:
                ctxt['advice'] = "Title can't be a void value."
            elif len(request.POST['title']) > maxTitleSize:
                ctxt['advice'] = 'The title max size is ' + str(maxTitleSize) + ' characters.'
            elif len(request.POST['description']) > maxDescriptionSize:
                ctxt['advice'] = 'The description max size is ' + str(maxDescriptionSize) + ' characters.'
            else:
                ctxt['advice'] = 'An error occurred.'
    return render(request, 'create_tasks.html', ctxt)

@login_required
def taskDetail(request, taskId, boardId):
    priorityChoices = Task.priorityChoices
    status = Status.objects.filter(user = request.user)
    myBoard = get_object_or_404(Board, pk = boardId, user = request.user)
    myTask = get_object_or_404(Task, pk = taskId, user = request.user)
    minDate = timezone.now()
    formatMinDate = minDate.strftime("%Y-%m-%d")
    deadline = myTask.deadline
    formatDeadline = None
    if deadline:
        formatDeadline = deadline.strftime("%Y-%m-%d")
    ctxt = {
        'myTask': myTask,
        'myStatus': status,
        'taskDetail': True,
        'priorityChoices': priorityChoices,
        'formatDeadline' : formatDeadline,
        'formatMinDate' : formatMinDate,
        'myBoard' : myBoard,
    }
    if request.method == 'POST':    
        try:
            form = TaskForm(request.POST, instance = myTask)
            form.save()
            return redirect('tasks', boardId = boardId)
        except ValueError:
            maxTitleSize = settings.GLOBAL_SETTINGS['TITLE_TEXT_INPUT']
            maxDescriptionSize = settings.GLOBAL_SETTINGS['AREA_TEXT_INPUT']
            if len(request.POST['title']) == 0:
                ctxt['advice'] = "Title can't be a void value."
            elif len(request.POST['title']) > maxTitleSize:
                ctxt['advice'] = 'The title max size is ' + str(maxTitleSize) + ' characters.'
            elif len(request.POST['description']) > maxDescriptionSize:
                ctxt['advice'] = 'The description max size is ' + str(maxDescriptionSize) + ' characters.'
            else:
                ctxt['advice'] = 'An error occurred.'
    return render(request, 'create_tasks.html', ctxt)

@login_required
def taskDeleted(request, taskId, boardId):
    myTask = get_object_or_404(Task, pk = taskId, user = request.user)
    myTask.delete()
    return redirect('tasks', boardId = boardId)

@login_required
def createStatus(request, boardId):
    myBoard = get_object_or_404(Board, pk = boardId, user = request.user)
    ctxt = {
        'myBoard': myBoard
    }
    if request.method == 'POST':
        try:
            form = StatusForm(request.POST)
            newStatus = form.save(commit = False)
            newStatus.user = request.user
            newStatus.save()
            return redirect('tasks', boardId = boardId)
        except ValueError:
            maxTitleSize = settings.GLOBAL_SETTINGS['TITLE_TEXT_INPUT']
            if len(request.POST['title']) == 0:
                ctxt['advice'] = "Title can't be a void value." 
            elif len(request.POST['title']) > maxTitleSize:
                ctxt['advice'] = 'The title max size is ' + str(maxTitleSize) + ' characters.'
            else:
                ctxt['advice'] = 'An error occurred.'
    return render(request, 'create_status.html', ctxt)

@login_required
def statusDetail(request, statusId, boardId):
    myBoard = get_object_or_404(Board, pk = boardId, user = request.user)
    myStatus = get_object_or_404(Status, pk = statusId, user = request.user)
    ctxt = {
        'myStatus': myStatus,
        'statusDetail': True,
        'myBoard': myBoard,
    }
    if request.method == 'POST':
        try:
            form = StatusForm(request.POST, instance = myStatus)
            form.save()
            return redirect('tasks', boardId = boardId)
        except ValueError:
            maxTitleSize = settings.GLOBAL_SETTINGS['TITLE_TEXT_INPUT']
            if len(request.POST['title']) == 0:
                ctxt['advice'] = "Title can't be a void value." 
            elif len(request.POST['title']) > maxTitleSize:
                ctxt['advice'] = 'The title max size is ' + str(maxTitleSize) + ' characters.'
            else:
                ctxt['advice'] = 'An error occurred.'
    return render(request, 'create_status.html', ctxt)

@login_required
def statusDeleted(request, statusId, boardId):
    myStatus = get_object_or_404(Status, pk = statusId, user = request.user)
    myStatus.delete()
    return redirect('tasks', boardId = boardId)

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    ctxt = {}
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('home')
        if len(request.POST['username']) == 0 :
            ctxt['advice'] = "Username can't be a void value."
        elif len(request.POST["password"]) == 0:
            ctxt['advice'] = "Password can't be a void value."
        else:
            ctxt ['advice'] = 'User or password are incorrect.'
    return render(request, 'signin.html', ctxt)

def signup(request):
    ctxt = {}
    if request.method == 'POST':
        maxUsernameSize = settings.GLOBAL_SETTINGS['TITLE_TEXT_INPUT']
        minPasswordSize = settings.GLOBAL_SETTINGS['PASSWORD_MIN_INPUT']
        maxPasswordSize = settings.GLOBAL_SETTINGS['PASSWORD_MAX_INPUT']
        if request.POST['username'] and (len(request.POST['password1']) >= minPasswordSize and len(request.POST['password1']) < maxPasswordSize) and request.POST['password1'] == request.POST['password2']:
            try:
                newUser = None
                newUser = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                newUser.save()
                login(request, newUser)
                return redirect('home')
            except IntegrityError:
                ctxt ['advice'] = "User already exists."
        else:
            if len(request.POST['username']) == 0:
                ctxt ['advice'] = "Username cant'be a void value."
            elif len(request.POST['username']) > maxUsernameSize:
                ctxt ['advice'] = "The username max size is " + str(maxUsernameSize) + " characters."
            elif len(request.POST['password1']) < minPasswordSize:
                ctxt ['advice'] = "Use at least "+ str(minPasswordSize) + " characters in the password."
            elif len(request.POST['password1']) > maxPasswordSize:
                ctxt ['advice'] = "The password max size is " + str(maxPasswordSize) + " characters."
            elif request.POST['password1'] != request.POST['password2']:
                ctxt ['advice'] = "the passwords don't match."
            else:
                ctxt['advice'] = 'An error occurred.'
    return render(request, 'signup.html', ctxt)