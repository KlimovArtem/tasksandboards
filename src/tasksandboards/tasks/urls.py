from django.urls import path

from tasks.views import TasksList


app_name = 'tasks'

urlpatterns = [
    path('', TasksList.as_view(), name='tasks_list'),
]
