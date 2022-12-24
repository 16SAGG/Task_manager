from django.urls import path
from .views import home, signup, tasks, signout, signin, createTasks, taskDetail, taskDeleted, createStatus, statusDetail, statusDeleted

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('signout/', signout, name='signout'),
    path('signin/', signin, name='signin'),
    path('tasks/', tasks, name='tasks'),
    path('tasks/<int:choiceStatId>/create/', createTasks, name='createTasks'),
    path('tasks/<int:taskId>/', taskDetail, name='taskDetail'),
    path('tasks/<int:taskId>/deleted/', taskDeleted, name='taskDeleted'),
    path('tasks/create/status', createStatus, name='createStatus'),
    path('tasks/<int:statusId>/status/detail', statusDetail, name='statusDetail'),
    path('tasks/<int:statusId>/status/deleted', statusDeleted, name='statusDeleted'),
]