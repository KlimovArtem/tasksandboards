from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class SigninForm(AuthenticationForm):
    email = forms.EmailField(required=True)
    password = forms.PasswordInput()

    class Meta:
        model = get_user_model()
        fields = [  # noqa: RUF012
            'email',
            'password',
        ]


class SignupForm(UserCreationForm):
    email = forms.CharField(label='Почта')
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(),
    )

    class Meta:
        model = get_user_model()
        fields = [  # noqa: RUF012
            'email',
            'password1',
            'password2',
        ]
