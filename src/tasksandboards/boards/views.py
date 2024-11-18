from calendar import c
from django.db.models import QuerySet
from django.views.generic import TemplateView, ListView

from boards.models import *


class BoardsList(ListView):
    template_name = 'boards/boards_list.html'

    def get_queryset(self):
        boards = QuerySet()
        [boards.union(board.objects.all()) for board in Board.__subclasses__()]
        return boards


class StartPageView(TemplateView):
    template_name = 'core/start_page.html'
