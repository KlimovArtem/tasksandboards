from core.views import StartPageView
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('boards/', include('boards.urls', namespace='boards')),
    path('tasks/', include('tasks.urls', namespace='tasks')),
    path('', StartPageView.as_view(), name='start_page'),

]
