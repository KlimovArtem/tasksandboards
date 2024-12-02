from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.transaction import commit
from django.views.generic import CreateView, TemplateView, ListView

from accounts.views import HtmxOnlyMixin
from boards.forms import CreateKanbanForm, ColumnFormset
from boards.models.kanban import Kanban


class BoardsList(HtmxOnlyMixin, ListView):
    context_object_name = 'boards'
    template_name = 'boards/boards_list.html'

    def get_queryset(self):
        return Kanban.objects.filter(owner=self.request.user)

class CreateBoard(LoginRequiredMixin, TemplateView):
    template_name = 'boards/create_board.html'

class CreateKanban(LoginRequiredMixin, CreateView):
    model = Kanban
    template_name = 'boards/create_kanban.html'
    form_class = CreateKanbanForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        data = kwargs.get('data', {})
        data.update({'owner': self.request.user})
        kwargs['data'] = data
        return kwargs

