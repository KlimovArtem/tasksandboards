from django.db.transaction import commit
from django.http import HttpResponseRedirect
from django.template.context_processors import request
from django.urls import reverse_lazy
from accounts.views import HtmxOnlyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, TemplateView

from boards.forms import ColumnFormset, CreateKanbanForm
from boards.models.kanban import Kanban, Column


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
    success_url = reverse_lazy('success')

    def get_context_data(self, **kwargs):
        if 'formset' not in kwargs:
            kwargs['formset'] = ColumnFormset(prefix='column', queryset=Column.objects.none())
        return super().get_context_data(**kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        formset = ColumnFormset(prefix='column', data=self.request.POST, queryset=Column.objects.none())
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)
    
    def form_valid(self, form, formset):
        board = form.save(commit=False)
        board.owner = self.request.user
        board.save()
        columns = formset.save(commit=False)
        for column in columns:
            column.board = board
            column.save()
        self.object = board
        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form, formset):
        return self.render_to_response(self.get_context_data(form=form, formset=formset))
