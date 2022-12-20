from django.urls import path
from .views import home, signup, tasks, signout, signin, createTasks, taskDetail

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('signout/', signout, name='signout'),
    path('signin/', signin, name='signin'),
    path('tasks/', tasks, name='tasks'),
    path('tasks/create/', createTasks, name='createTasks'),
    path('tasks/<int:taskId>/', taskDetail, name='taskDetail'),
]