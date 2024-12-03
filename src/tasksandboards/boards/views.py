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

    def post(self, request, *args, **kwargs):
        board_form = self.get_form()
        columns_form = ColumnsWidget(**self.get_form_kwargs())
        if board_form.is_valid() and columns_form.is_valid():
            return self.form_valid(board_form, columns_form)
        else:
            return self.form_invalid(board_form, columns_form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        data = kwargs.get('data', {})
        data.update({'owner': self.request.user})
        kwargs['data'] = data
        return kwargs

    def form_valid(self, board_form, columns_form):
        """If the form is valid, save the associated model."""
        board = board_form.save(commit=False)
        columns = columns_form.save(commit=False)
        board.columns.set(columns, bulk=False)
        self.object = board.save()
        return super().form_valid(board_form)

    def form_invalid(self, board_form, columns_form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(board_form=board_form, columns_form=columns_form))

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['columns_form'] = ColumnsWidget(**self.get_form_kwargs())
        data['board_form'] = data['form']
        return data
