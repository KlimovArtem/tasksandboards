from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from django.core import mail
from django.db.models import fields
from django.test import Client, RequestFactory

from tasksandboards.accounts.models import Account
from tasksandboards.accounts.views import SigninView


class TestLogin:
    def test_login_url(self, client: Client):
        response = client.get('accounts/login/')
        assert response.status_code == HTTPStatus.OK, f'Ресурс не доступен, код ответа {response.status_code }.'
        assert response.status_code != HTTPStatus.NOT_FOUND, 'Ресурс не доступен, код ответа 404. Проверь *urls.py*.'

    def test_login_view(self, client: Client):
        response = client.get('accounts/login/')
        assert (
            response.template == 'accounts/login.html'
        ), 'Ошибка!! Класс LoginView не использует шаблон `account/login.html'


class TestSignup:
    def non_htmx_request(self, client):
        response = client.get('accounts/signup/')
        assert (
            response.status_code == HTTPStatus.BAD_REQUEST
        ), 'Пользователь имеет досту к служебному ресурсую, проверь *views.py*.'

        response = client.post('accounts/signup/')
        assert (
            response.status_code == HTTPStatus.BAD_REQUEST
        ), 'Пользователь имеет досту к служебному ресурсую, проверь *views.py*.'

    def test_nodata_signup(self, client):
        invalid_response = client.post(
            'accounts/signup/',
            header={'HX-Request': 'true'},
        )
        assert (
            invalid_response.status_code == HTTPStatus.BAD_REQUEST
        ), 'Пользователь может зарегестрироваться не передовая данных для регистрации.'
        assert (
            'email' in invalid_response.context['form'].errors
        ), 'Форма не передаёт информацию об ошибках в поле `email`'
        assert (
            'password' in invalid_response.context['form'].errors
        ), 'Форма не передаёт информацию об ошибках в поле `password`'
        assert (
            'confirm_password' in invalid_response.context['form'].errors
        ), 'Форма не передаёт информацию об ошибках в поле `confirm_password`'

    def test_signup_context(self, client: Client):
        response = client.get('accounts/signup/', header={'HX-Request': 'true'})

        assert (
            response.template == 'accounts/signup.html'
        ), 'Ошибка!! Класс SignupView не использует шаблон `account/signup.html'
        assert 'form' in response.context, 'В контекст не передан объект формы.'
        assert 'email' in response.context['form'].fields, 'В форме нет поля `email`, проверь *forms.py*.'
        assert 'password' in response.context['form'].fields, 'В форме нет поля `password`, проверь *forms.py*.'
        assert (
            'confirm_password' in response.context['form'].fields
        ), 'В форме нет поля `confirm_password`, проверь *forms.py*.'
        assert response.context['form'].fields['email'].required, 'Проверь что поле `email` обязательно для заполнения.'
        assert (
            response.context['form'].fields['password'].required
        ), 'Проверь что поле `email` обязательно для заполнения.'
        assert (
            response.context['form'].fields['confirm_password'].required
        ), 'Проверь что поле `email` обязательно для заполнения.'

    @pytest.mark.django_db(transaction=True)
    def test_valid_user_signup(self, client: Client, django_user_model):
        outbox_before_count = len(mail.outbox)
        valid_data = {
            'email': 'testuser@email.com',
            'password': 1234567,
            'confirm_password': 1234567,
        }
        response = client.get('accounts/signup/', headers={'HX-Request': 'true'})
        outbox_after = mail.outbox

        assert response.status_code == HTTPStatus.OK, f'Ресурс не доступен, код ответа {response.status_code }.'
        assert response.status_code != HTTPStatus.NOT_FOUND, 'Ресурс не доступен, код ответа 404. Проверь *urls.py*.'

        new_user = django_user_model.objects.filter(email=valid_data['email'])
        assert new_user.exists(), 'Корректный запрос должен создать нового пользователя.'
        assert (
            len(outbox_after) == outbox_before_count + 1
        ), 'Если отправлен корректный запрос - должен быть отправлено письмо с кодом подтверждения.'

        assert (
            valid_data['email'] == outbox_after.to
        ), 'Если отправлен корректный запрос - письмо должно быть отправленно на правильный адрес'
        new_user.delete()

    @pytest.mark.django_db(transaction=True)
    def test_invalid_user_signup(self, client: Client, django_user_model):
        pass


class TestSignin:
    def test_signin_get(self, rf: RequestFactory, client: Client):
        htmx_request = rf.get('accounts/signin/')
        htmx_request.META['HX-Request'] = 'true'
        htmx_response = SigninView.as_view()(htmx_request)
        response = client.get('accounts/signin/')

        assert (
            response.status_code == HTTPStatus.BAD_REQUEST
        ), 'Пользователь имеет досту к служебному ресурсую, проверь *views.py*.'
        assert (
            htmx_response.status_code == HTTPStatus.OK
        ), f'Ресурс не доступен, код ответа {htmx_response.status_code }.'
        assert (
            htmx_response.status_code != HTTPStatus.NOT_FOUND
        ), 'Ресурс не доступен, код ответа 404. Проверь *urls.py*.'
        assert (
            htmx_response.template == 'accounts/signup.html'
        ), 'Ошибка!! Класс SignupView не использует шаблон `account/signup.html'
        assert 'form' in htmx_response.context, 'В контекст не передан объект формы.'
        assert 'email' in htmx_response.context['form'].fields, 'В форме нет поля `email`, проверь *forms.py*.'
        assert 'password' in htmx_response.context['form'].fields, 'В форме нет поля `password`, проверь *forms.py*.'
        assert (
            htmx_response.context['form'].fields['email'].required
        ), 'Проверь что поле `email` обязательно для заполнения.'
        assert (
            htmx_response.context['form'].fields['password'].required
        ), 'Проверь что поле `email` обязательно для заполнения.'

    @pytest.mark.django_db(transaction=True)
    def test_signin_view_post(self, rf: RequestFactory, client: Client):
        user = get_user_model().objects.create(
            email='testuser@email.com',
            password=1234567,
        )
        htmx_request = rf.post(
            'accounts/signin/',
            {
                'email': 'testuser@email.com',
                'password': 1234567,
            },
        )
        htmx_request_wrong_data = rf.post(
            'accounts/signin/',
            {
                'email': 't@stuser@124email.com',
                'password': 1234567,
            },
        )
        htmx_request.META['HX-Request'] = 'true'
        htmx_request_wrong_data.META['HX-Request'] = 'true'
        htmx_response = SigninView.as_view()(htmx_request)
        response_with_wrong_data = SigninView.as_view()(htmx_request_wrong_data)
        assert (
            htmx_response.status_code == HTTPStatus.SEE_OTHER
        ), 'Пользователь не перенаправляется на запрашиваемую страницу.'
        assert user.is_authenticated, 'Пользователь не авторизовался, проверь *views.py*.'
        assert (
            response_with_wrong_data.context['form'].fields['email'].errors
        ), 'Форма не передаёт информацию об ошибках в поле `email`'
        assert (
            response_with_wrong_data.context['form'].fields['password'].errors
        ), 'Форма не передаёт информацию об ошибках в поле `password`'


class TestAccountModel:
    def test_account_model(self):
        model_fields = Account._meta.fields
        email_field = next(field for field in model_fields if field.hasattr('email'))

        assert email_field is not None, 'Модель `Account` должна содержать атрибут `email`.'
        assert isinstance(
            email_field,
            fields.EmailField,
        ), 'Поле `email` должно быть типа `EmailField`'
        assert email_field.unique, 'Поле `email` должно быть уникальным.'
