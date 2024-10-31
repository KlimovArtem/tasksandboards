from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError


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

class ConfirmSignupForm(forms.Form):
    num1 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(
            attrs={'class': 'confirm_signup_fields', 'inputmod': 'numeric'}
        )
    )
    num2 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(
            attrs={'class': 'confirm_signup_fields', 'inputmod': 'numeric'}
        )
    )
    num3 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(
            attrs={'class': 'confirm_signup_fields', 'inputmod': 'numeric'}
        )
    )
    num4 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(
            attrs={'class': 'confirm_signup_fields', 'inputmod': 'numeric'}
        )
    )

    def clean(self) -> dict:
        cleaned_data = super().clean()
        confirm_code = self.kwargs.get('confirm_code')
        user_code = f'{cleaned_data["num1"]}{cleaned_data["num2"]}{cleaned_data["num3"]}{cleaned_data["num4"]}'
        if not confirm_code:
            raise ValidationError("Код подтверждения не был выслан.")
        if user_code != confirm_code:
            raise ValidationError("Не верный код подтверждения.")
        return cleaned_data
