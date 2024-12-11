from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import BaseUserCreationForm
from django.core.exceptions import ValidationError
from django.utils.text import capfirst
from django.utils.translation import gettext_lazy


UserModel = get_user_model()


class SigninForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label=gettext_lazy('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    error_messages = {
        'invalid_login': gettext_lazy(
            'Please enter a correct %(email)s and password. Note that both fields may be case-sensitive.',
        ),
        'inactive': gettext_lazy('This account is inactive.'),
    }

    def __init__(self, request=None, *args, **kwargs) -> None:
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.email_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)  # noqa: SLF001
        email_max_length = self.email_field.max_length or 254
        self.fields['email'].max_length = email_max_length
        self.fields['email'].widget.attrs['maxlength'] = email_max_length
        if self.fields['email'].label is None:
            self.fields['email'].label = capfirst(self.email_field.verbose_name)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(
                self.request,
                email=email,
                password=password,
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """  # noqa: D205, D401
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'email': self.email_field.verbose_name},
        )


class SignupForm(BaseUserCreationForm):
    class Meta:
        model = UserModel
        fields = [
            'email',
            'password1',
            'password2',
        ]


class ConfirmSignupForm(forms.Form):
    def __init__(self, request=None, *args, **kwargs) -> None:
        self.request = request
        super().__init__(*args, **kwargs)

    error_messages = {
        'wrong_code': gettext_lazy('Wrong confirm code.'),
    }

    num1 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(
            attrs={'class': 'confirm_signup_fields', 'inputmod': 'numeric'},
        ),
    )
    num2 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(
            attrs={'class': 'confirm_signup_fields', 'inputmod': 'numeric'},
        ),
    )
    num3 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(
            attrs={'class': 'confirm_signup_fields', 'inputmod': 'numeric'},
        ),
    )
    num4 = forms.CharField(
        max_length=1,
        widget=forms.TextInput(
            attrs={'class': 'confirm_signup_fields', 'inputmod': 'numeric'},
        ),
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        confirm_code = self.request.session.get('confirm_code')
        user_code = f"{cleaned_data['num1']}{cleaned_data['num2']}{cleaned_data['num3']}{cleaned_data['num4']}"
        if user_code != confirm_code:
            raise ValidationError(
                self.error_messages['wrong_code'],
                code='wrong_code',
            )
        return super().clean()
