from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class StartPageView(LoginRequiredMixin, TemplateView):
    template_name = 'core/start_page.html'


class SuccessView(TemplateView):
    """View for test success form"""

    template_name = 'core/success.html'
