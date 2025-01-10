from django.views.generic import ListView

from tasks.models import Task


class TasksList(ListView):
    model = Task
    template_name = 'tasks/tasks_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        current_board = self.request.session['current_board']
        filter = dict()
        for key, value in self.request.GET.items():
            if isinstance(value, list):
                if value.len() == 1:
                    value = value[0]
            if value.isdigit():
                value = int(value)
            filter[key] = value

        queryset = super().get_queryset().filter(board=current_board, **filter)
        return queryset
