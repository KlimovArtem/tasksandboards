from core.views import StartPageView, SuccessView
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('boards/', include('boards.urls', namespace='boards')),
    path('', StartPageView.as_view(), name='start_page'),
    path('', include('django_components.urls')),
    path('success', SuccessView.as_view(), name='success'),
]
