from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from accounts.views import HtmxOnlyMixin
from boards.forms import ColumnFormset, CreateKanbanForm
from boards.models.kanban import Column, Kanban


class BoardsList(HtmxOnlyMixin, ListView):
    context_object_name = 'boards'
    template_name = 'boards/boards_list.html'

    def get_queryset(self):
        return Kanban.objects.filter(owner=self.request.user).values('slug', 'name')


class CreateBoard(LoginRequiredMixin, TemplateView):
    template_name = 'boards/create_board.html'


class CreateKanban(LoginRequiredMixin, CreateView):
    model = Kanban
    template_name = 'boards/create_kanban.html'
    form_class = CreateKanbanForm

    def get_context_data(self, **kwargs):
        if 'formset' not in kwargs:
            kwargs['formset'] = ColumnFormset(prefix='column', queryset=Column.objects.none())
        return super().get_context_data(**kwargs)

    def post(self, *args, **kwargs):
        self.object = None
        form = self.get_form()
        formset = ColumnFormset(prefix='column', data=self.request.POST, queryset=Column.objects.none())
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
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


class BoardContentView(LoginRequiredMixin, DetailView):
    template_name = 'boards/kanban_mockup.html'
    context_object_name = 'board'
    slug_url_kwarg = 'board_slug'

    def get_queryset(self):
        queryset = Kanban.objects.filter(owner=self.request.user)
        return queryset
