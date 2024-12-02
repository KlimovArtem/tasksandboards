from django import forms
from django.utils.translation import gettext_lazy 

from boards.models import Kanban
from boards.models.kanban import Column


class CreateKanbanForm(forms.ModelForm):

    class Meta:
        model = Kanban
        fields = ['name', 'description']
        labels = {
            'name': gettext_lazy('Название'),
            'description': gettext_lazy('Описание'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-field-text'}),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-field-textarea',
                    'rows': 6,
                    'cols': 27,
                    'wrap': 'soft',
                    'required': False,
                }
            )
        }

    