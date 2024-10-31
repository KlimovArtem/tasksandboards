from django.contrib.auth.views import LoginView as BaseSigninView
from django.core.mail import send_mail
from django.views.generic import CreateView, TemplateView, FormView
from django.urls import reverse_lazy

from accounts.forms import SigninForm, SignupForm, ConfirmSignupForm
from accounts.utilits import get_confirm_code


class HtmxOnlyMixin:
    pass


class LoginView(TemplateView):
    template_name = 'accounts/login.html'


class SigninView(HtmxOnlyMixin, BaseSigninView):
    form_class = SigninForm
    template_name = 'accounts/signin.html'


class SignupView(HtmxOnlyMixin, CreateView):
    success_url = reverse_lazy('accounts:confirm_signup')
    form_class = SignupForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.username = self.object.email
        self.object.save()
        self.request.session['user_email'] = self.object.email
        return super().form_valid(form)


class ConfirmSignupView(FormView):
    form_class = ConfirmSignupForm
    template_name = 'accounts/confirm_signup.html'
    success_url = reverse_lazy('accounts:login')

    def get(self, request, *args, **kwargs):
        confirm_code = get_confirm_code()
        self.request.session['confirm_code'] = confirm_code
        send_mail(
            subject="TestSigup email",
            from_email="sometest@email.com",
            message=confirm_code,
            recipient_list=[self.request.session.get('user_email'),]
        )
        return super().get(request, *args, **kwargs)
