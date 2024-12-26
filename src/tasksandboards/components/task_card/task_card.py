from django_components import Component, register


@register("task_card")
class TaskCard(Component):
    template_name = 'task_card.html'

    class Media:
        js = "task_card.js"
        css = "task_card.css"

    def get_context_data(self):
        return {
            'title': 'Загаловок заметки',
            'body': 'Тело карточки',
        }
