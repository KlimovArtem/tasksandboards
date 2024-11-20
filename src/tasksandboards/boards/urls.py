from django.urls import path

from boards.views import BoardsList, CreateBoard, CreateKanban


app_name = 'boards'

urlpatterns = [
    path('', BoardsList.as_view(), name='boards_list'),
    path('create/', CreateBoard.as_view(), name='create'),
    path('create/kanban', CreateKanban.as_view(), name='create_kanban'),
]
