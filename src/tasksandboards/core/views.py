from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class StartPageView(LoginRequiredMixin, TemplateView):
    template_name = 'core/start_page.html'
