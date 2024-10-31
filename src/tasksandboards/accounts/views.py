from django.contrib.auth.views import LoginView as BaseSigninView
from django.views.generic import CreateView, TemplateView

from accounts.forms import SigninForm, SignupForm


class HtmxOnlyMixin:
    pass


class LoginView(TemplateView):
    template_name = 'accounts/login.html'


class SigninView(HtmxOnlyMixin, BaseSigninView):
    form_class = SigninForm
    template_name = 'accounts/signin.html'


class SignupView(HtmxOnlyMixin, CreateView):
    form_class = SignupForm
    template_name = 'accounts/signup.html'
