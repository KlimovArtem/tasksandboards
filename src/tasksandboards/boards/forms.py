from django import forms
from django.utils.translation import gettext_lazy

from boards.models import Kanban
from boards.models.kanban import Column


class ColumnForm(forms.ModelForm):
    class Meta:
        model = Column
        fields = ['name', 'position']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'col-name', 'readonly': True}),
            'position': forms.TextInput(attrs={'class': 'col-pos', 'readonly': True}),
        }


ColumnFormset = forms.modelformset_factory(
    Column,
    form=ColumnForm,
    extra=0,
)


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
                },
            ),
        }
