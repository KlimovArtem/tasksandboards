from django.urls import path

from boards.views import StartPageView, BoardsList


app_name = 'boards'

urlpatterns = [
    path('', StartPageView.as_view(), name='start_page'),
    path('boards/', BoardsList.as_view(), name='boards_list'),
]
