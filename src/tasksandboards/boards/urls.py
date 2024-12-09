from django.urls import path

from boards.views import BoardsList, CreateBoard, CreateKanban, BoardContentView


app_name = 'boards'

urlpatterns = [
    path('', BoardsList.as_view(), name='boards_list'),
    path('create/', CreateBoard.as_view(), name='create'),
    path('create/kanban', CreateKanban.as_view(), name='create_kanban'),
    path('<slug:board_slug>/tasks', BoardContentView.as_view(), name='board_tasks'),
]
