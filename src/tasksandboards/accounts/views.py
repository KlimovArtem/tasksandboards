from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView as BaseSigninView
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView

from accounts.forms import ConfirmSignupForm, SigninForm, SignupForm
from accounts.utilits import get_confirm_code


class HtmxOnlyMixin:
    """Allows only htmx requests."""

    def dispatch(self, request, *args, **kwargs):
        if not request.htmx:
            raise PermissionDenied('Ресурс только для внутреннего пользования.')
        return super().dispatch(request, *args, **kwargs)


class LoginView(TemplateView):
    template_name = 'accounts/login.html'


class SigninView(HtmxOnlyMixin, BaseSigninView):
    form_class = SigninForm
    template_name = 'accounts/signin.html'

    def get_success_url(self) -> str:
        return reverse_lazy('accounts:success_login')


class SignupView(HtmxOnlyMixin, CreateView):
    success_url = reverse_lazy('accounts:confirm_signup')
    form_class = SignupForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        self.object = form.save()
        self.request.session['user_email'] = self.object.email
        return super().form_valid(form)


class ConfirmSignupView(HtmxOnlyMixin, FormView):
    form_class = ConfirmSignupForm
    template_name = 'accounts/confirm_signup.html'
    success_url = reverse_lazy('accounts:login')

    def get(self, request, *args, **kwargs):
        confirm_code = get_confirm_code()
        self.request.session['confirm_code'] = confirm_code
        send_mail(
            subject='TestSigup email',
            from_email='sometest@email.com',
            message=confirm_code,
            recipient_list=[
                self.request.session.get('user_email'),
            ],
        )
        return super().get(request, *args, **kwargs)


    def form_valid(self, form):
        user = get_user_model().objects.get(email=self.request.session['user_email'])
        user.is_active = True
        user.save()
        self.request.session['user_email'] = ''
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs