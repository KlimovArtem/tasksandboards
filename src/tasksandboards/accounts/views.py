from django.contrib.auth.views import LoginView as BaseSigninView
from django.views.generic import TemplateView

from accounts.forms import SigninForm


class LoginView(TemplateView):
    template_name = 'accounts/login.html'


class SigninView(BaseSigninView):
    form_class = SigninForm
    template_name = 'accounts/signin.html'
