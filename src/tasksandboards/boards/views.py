from django.db.models import QuerySet
from django.http import Http404
from django.utils.translation import gettext_lazy
from django.views.generic import TemplateView, ListView

from boards.models import *


class BoardsList(ListView):
    context_object_name = 'boards'
    template_name = 'boards/boards_list.html'

    def get_queryset(self):
        boards = QuerySet()
        for board in Board.__subclasses__():
            boards.union(board.objects.all())
        return ['Канбан', 'Блокнот']


class StartPageView(TemplateView):
    template_name = 'core/start_page.html'
