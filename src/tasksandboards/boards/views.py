from accounts.views import HtmxOnlyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, TemplateView

from boards.forms import ColumnsWidget, CreateKanbanForm
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

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['formset'] = ColumnsWidget()
        return data
