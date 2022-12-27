from django.urls import path
from .views import home, signup, tasks, signout, signin, createTasks, taskDetail, taskDeleted, createStatus, statusDetail, statusDeleted, createBoard, boardDetail, boardDeleted

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('signout/', signout, name='signout'),
    path('signin/', signin, name='signin'),
    path('board/create', createBoard, name='createBoard'),
    path('board/<int:boardId>', boardDetail, name='boardDetail'),
    path('board/<int:boardId>/deleted/', boardDeleted, name='boardDeleted'),
    path('board/<int:boardId>/tasks/', tasks, name='tasks'),
    path('board/<int:boardId>/tasks/<int:choiceStatId>/create/', createTasks, name='createTasks'),
    path('board/<int:boardId>/tasks/<int:taskId>/', taskDetail, name='taskDetail'),
    path('board/<int:boardId>/tasks/<int:taskId>/deleted/', taskDeleted, name='taskDeleted'),
    path('board/<int:boardId>/tasks/create/status', createStatus, name='createStatus'),
    path('board/<int:boardId>/tasks/<int:statusId>/status/detail', statusDetail, name='statusDetail'),
    path('board/<int:boardId>/tasks/<int:statusId>/status/deleted', statusDeleted, name='statusDeleted'),
]