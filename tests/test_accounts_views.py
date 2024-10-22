from http import HTTPStatus

import pytest
from django.core import mail
from django.urls import reverse_lazy


class TestLogin:
    LOGIN_URL = reverse_lazy('accounts:login')

    def test_login_url(self, client):
        response = client.get(TestLogin.LOGIN_URL)
        assert (
            response.status_code == HTTPStatus.OK
        ), f'Ресурс `accounts/login/` не доступен, код ответа {response.status_code }.'
        assert (
            response.status_code != HTTPStatus.NOT_FOUND
        ), 'Ресурс `accounts/login/` не доступен, код ответа 404. Проверь *urls.py*.'

    def test_login_view(self, client):
        response = client.get(TestLogin.LOGIN_URL)
        assert (
            response.context_data['view'].template_name == 'accounts/login.html'
        ), 'Ошибка!! Класс LoginView не использует шаблон `account/login.html'


class TestSignup:
    SIGNUP_URL = reverse_lazy('accounts:signup')

    def non_htmx_request(self, client):
        response = client.get(TestSignup.SIGNUP_URL)
        assert (
            response.status_code == HTTPStatus.BAD_REQUEST
        ), 'Пользователь имеет досту к служебному ресурсу `accounts/signup/, проверь *views.py*.'

        response = client.post(TestSignup.SIGNUP_URL)
        assert (
            response.status_code == HTTPStatus.BAD_REQUEST
        ), 'Пользователь имеет досту к служебному ресурсую `accounts/signup/, проверь *views.py*.'

    def test_nodata_signup(self, client):
        invalid_response = client.post(
            TestSignup.SIGNUP_URL,
            header={'HX-Request': 'true'},
        )
        assert (
            invalid_response.status_code == HTTPStatus.BAD_REQUEST
        ), 'Пользователь может зарегестрироваться не передавая данных для регистрации.'
        assert (
            'email' in invalid_response.context_data['form'].errors
        ), 'Форма не передаёт информацию об ошибках в поле `email`'
        assert (
            'password' in invalid_response.context_data['form'].errors
        ), 'Форма не передаёт информацию об ошибках в поле `password`'
        assert (
            'confirm_password' in invalid_response.context_data['form'].errors
        ), 'Форма не передаёт информацию об ошибках в поле `confirm_password`'

    def test_signup_context(self, client):
        response = client.get(TestSignup.SIGNUP_URL, header={'HX-Request': 'true'})

        assert response.status_code == HTTPStatus.OK, f'Ресурс не доступен, код ответа {response.status_code }.'
        assert response.status_code != HTTPStatus.NOT_FOUND, 'Ресурс не доступен, код ответа 404. Проверь *urls.py*.'

        assert (
            response.context_data['view'].template_name == 'accounts/signup.html'
        ), 'Ошибка!! Класс SignupView не использует шаблон `account/signup.html'
        assert 'form' in response.context_data, 'В контекст не передан объект формы.'
        assert 'email' in response.context_data['form'].fields, 'В форме нет поля `email`, проверь *forms.py*.'
        assert 'password' in response.context_data['form'].fields, 'В форме нет поля `password`, проверь *forms.py*.'
        assert (
            'confirm_password' in response.context_data['form'].fields
        ), 'В форме нет поля `confirm_password`, проверь *forms.py*.'
        assert (
            response.context_data['form'].fields['email'].required
        ), 'Проверь что поле `email` обязательно для заполнения.'
        assert (
            response.context_data['form'].fields['password'].required
        ), 'Проверь что поле `password` обязательно для заполнения.'
        assert (
            response.context_data['form'].fields['confirm_password'].required
        ), 'Проверь что поле `confirm_password` обязательно для заполнения.'

    @pytest.mark.django_db(transaction=True)
    def test_valid_user_signup(self, client, django_user_model):
        outbox_before_count = len(mail.outbox)
        valid_data = {
            'email': 'testuser@email.com',
            'password': 1234567,
            'confirm_password': 1234567,
        }
        response = client.post(
            TestSignup.SIGNUP_URL,
            data=valid_data,
            headers={'HX-Request': 'true'},
        )
        outbox_after = mail.outbox

        assert response.status_code == HTTPStatus.CREATED, 'Корректный запрос должен возвращать код 201.'
        new_user = django_user_model.objects.filter(email=valid_data['email'])

        assert new_user.exists(), 'Корректный запрос не создаёт нового пользователя.'
        assert (
            len(outbox_after) == outbox_before_count + 1
        ), 'При корректном запросе не отправляется письмо с кодом подтверждения.'

        assert (
            valid_data['email'] == outbox_after.to
        ), 'Если отправлен корректный запрос - письмо должно быть отправленно на правильный адрес'
        new_user.delete()

    @pytest.mark.django_db(transaction=True)
    def test_invalid_user_signup(self, client, django_user_model):
        invalid_data = {
            'email': 'tes@^^tuser.mail.com',
            'password': '',
            'confirm_password': 2510561,
        }
        outbox_before_count = len(mail.outbox)
        users_number = django_user_model.objects.count()
        response = client.post(
            TestSignup.SIGNUP_URL,
            data=invalid_data,
            headers={'HX-Request': 'true'},
        )
        outbox_after_count = len(mail.outbox)

        assert response.status_code == HTTPStatus.BAD_REQUEST, 'При отправке некоректных данных не возвращается код 400'
        assert (
            django_user_model.objects.count() == users_number
        ), 'При отправке не коректных данных создатся пользователь.'
        assert (
            outbox_after_count == outbox_before_count
        ), 'При отправке не коректных данных отправляется письмо на почту пользователя'


class TestSignin:
    SIGNIN_URL = reverse_lazy('accounts:signin')

    def non_htmx_request(self, client):
        response = client.get(TestSignin.SIGNIN_URL)
        assert (
            response.status_code == HTTPStatus.BAD_REQUEST
        ), 'Пользователь имеет досту к служебному ресурсу `accounts/signin/`, проверь *views.py*.'

        response = client.post(TestSignin.SIGNIN_URL)
        assert (
            response.status_code == HTTPStatus.BAD_REQUEST
        ), 'Пользователь имеет досту к служебному ресурсу `accounts/signin/, проверь *views.py*.'

    def test_nodata_signin(self, client):
        empty_response = client.post(
            TestSignin.SIGNIN_URL,
            header={'HX-Request': 'true'},
        )
        # assert empty_response.status_code == HTTPStatus.BAD_REQUEST, noqa: RUF003
        # 'Не коректный запрос должен возвращать код 400.'   noqa: RUF003  # noqa: RUF003
        assert (
            'email' in empty_response.context_data['form'].errors
        ), 'Форма не передаёт информацию об ошибках в поле `email`'
        assert (
            'password' in empty_response.context_data['form'].errors
        ), 'Форма не передаёт информацию об ошибках в поле `password`'

    def test_signin_context(self, client):
        response = client.get(TestSignin.SIGNIN_URL, header={'HX-Request': 'true'})

        assert response.status_code == HTTPStatus.OK, f'Ресурс не доступен, код ответа {response.status_code }.'
        assert response.status_code != HTTPStatus.NOT_FOUND, 'Ресурс не доступен, код ответа 404. Проверь *urls.py*.'

        assert (
            response.context_data['view'].template_name == 'accounts/signin.html'
        ), 'Ошибка!! Класс SigninView не использует шаблон `account/signin.html'
        assert 'form' in response.context_data, 'В контекст не передан объект формы.'
        assert 'email' in response.context_data['form'].fields, 'В форме нет поля `email`, проверь *forms.py*.'
        assert 'password' in response.context_data['form'].fields, 'В форме нет поля `password`, проверь *forms.py*.'

        assert (
            response.context_data['form'].fields['email'].required
        ), 'Проверь что поле `email` обязательно для заполнения.'
        assert (
            response.context_data['form'].fields['password'].required
        ), 'Проверь что поле `password` обязательно для заполнения.'

    @pytest.mark.django_db(transaction=True)
    def test_valid_user_signin(self, client, django_user_model):
        valid_data = {
            'email': 'testuser@mail.com',
            'password': 1234567,
        }
        user = django_user_model.objects.create(**valid_data)
        response = client.post(
            TestSignin.SIGNIN_URL,
            data=valid_data,
            headers={'HX-Request': 'true'},
        )

        assert response.status_code == HTTPStatus.OK, 'Корректный запрос не возвращает код 200.'
        assert user.is_authenticated, 'При отправке корректных данных пользователь не был авторизован.'
        user.delete()


class TestLogout:
    LOGOUT_URL = reverse_lazy('accounts:logout')

    def test_valid_request(self, client, django_user_model):
        valid_data = {
            'email': 'testuser@mail.com',
            'password': 1234567,
        }
        user = django_user_model.objets.create(**valid_data)
        authenticated_client = client.force_login(user)
        response = authenticated_client.post(TestLogout.LOGOUT_URL)

        assert response.status_code == HTTPStatus.OK, 'Корректный запрос возвращает код 200.'
        assert response.status_code == HTTPStatus.NOT_FOUND, 'Ресурс `accounts/logout/` не найден проверь *urls.py*.'
        assert not authenticated_client.is_authenticated(), 'Пользователь не разлогинивается при коректном запросе.'
