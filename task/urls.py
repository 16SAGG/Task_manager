from django.urls import path
from .views import home, signup, tasks, signout, signin, createTasks, taskDetail, taskCompleted, taskDeleted, taskUncomplete

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('signout/', signout, name='signout'),
    path('signin/', signin, name='signin'),
    path('tasks/', tasks, name='tasks'),
    path('tasks/create/', createTasks, name='createTasks'),
    path('tasks/<int:taskId>/', taskDetail, name='taskDetail'),
    path('tasks/<int:taskId>/completed', taskCompleted, name='taskCompleted'),
    path('tasks/<int:taskId>/uncomplete', taskUncomplete, name='taskUncomplete'),
    path('tasks/<int:taskId>/deleted', taskDeleted, name='taskDeleted'),
]