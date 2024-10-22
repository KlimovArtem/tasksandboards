from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class SigninForm(AuthenticationForm):
    email = forms.EmailField(required=True)
    password = forms.PasswordInput()

    class Meta:
        model = get_user_model()
        fields = [  # noqa: RUF012
            'email',
            'password',
        ]
