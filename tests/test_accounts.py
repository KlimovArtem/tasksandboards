from boards.views import SignupView
from django.test import Client, RequestFactory


class TestViews:
    def test_login_view(self, client: Client):
        try:
            response = client.get('accounts/login/')
        except Exception as error:
            msg = f'Ресурс `accounts/login/` работает не коректно. Ошибка `{error}`.'
            raise AssertionError(msg)

        assert response.status_code == 200, f'Ресурс не доступен, код ответа {response.status_code }.'
        assert response.status_code != 404, 'Ресурс не доступен, код ответа 404. Проверь *urls.py*.'
        assert (
            response.template == 'accounts/login.html'
        ), 'Ошибка!! Класс LoginView не использует шаблон `account/signup.html'

    def test_signup_view(self, rf: RequestFactory, client: Client):
        try:
            htmx_request = rf.get('accounts/signup/')
            htmx_request.META['HX-Request'] = 'true'
            htmx_response = SignupView.as_view()(htmx_request)
            response = client.get('accounts/signup/')
        except Exception as error:
            msg = f'!!!Ошибка!!!! `{error}`'
            raise AssertionError(msg)

        assert response.status_code == 400, 'Пользователь имеет досту к служебному ресурсую, проверь *views.py*.'
        assert htmx_response.status_code == 200, f'Ресурс не доступен, код ответа {response.status_code }.'
        assert htmx_response.status_code != 404, 'Ресурс не доступен, код ответа 404. Проверь *urls.py*.'
        assert (
            htmx_response.template == 'accounts/signup.html'
        ), 'Ошибка!! Класс SignupView не использует шаблон `account/signup.html'
        assert 'form' in htmx_response.context, 'В контекст не передан объект формы.'
        assert 'email' in htmx_response.context['form'].fields, 'В форме нет поля `email`, проверь *forms.py*.'
        assert 'password' in htmx_response.context['form'].fields, 'В форме нет поля `password`, проверь *forms.py*.'
        assert (
            'confirm_password' in htmx_response.context['form'].fields
        ), 'В форме нет поля `confirm_password`, проверь *forms.py*.'
