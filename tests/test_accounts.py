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
    CONFIRM_SIGNUP_URL = reverse_lazy('accounts:confirm_signup')
    VALID_DATA = {
        'email': 'testuser@email.com',
        'password1': 'secret_password',
        'password2': 'secret_password',
    }

    def test_non_htmx_request(self, client):
        response = client.get(TestSignup.SIGNUP_URL)
        assert (
            response.status_code == HTTPStatus.FORBIDDEN
        ), 'Пользователь имеет досту к служебному ресурсу `accounts/signup/, проверь *views.py*.'

        response = client.post(TestSignup.SIGNUP_URL)
        assert (
            response.status_code == HTTPStatus.FORBIDDEN
        ), 'Пользователь имеет досту к служебному ресурсую `accounts/signup/, проверь *views.py*.'

    def test_nodata_signup(self, client):
        invalid_response = client.post(
            TestSignup.SIGNUP_URL,
            headers={'HX-Request': 'true'},
        )
        assert (
            invalid_response.status_code == HTTPStatus.OK
        ), 'Пользователь может зарегестрироваться не передавая данных для регистрации.'
        assert (
            'email' in invalid_response.context_data['form'].errors
        ), 'Форма не передаёт информацию об ошибках в поле `email`'
        assert (
            'password1' in invalid_response.context_data['form'].errors
        ), 'Форма не передаёт информацию об ошибках в поле `password`'
        assert (
            'password2' in invalid_response.context_data['form'].errors
        ), 'Форма не передаёт информацию об ошибках в поле `confirm_password`'

    def test_signup_context(self, client):
        response = client.get(TestSignup.SIGNUP_URL, headers={'HX-Request': 'true'})

        assert response.status_code == HTTPStatus.OK, f'Ресурс не доступен, код ответа {response.status_code }.'
        assert response.status_code != HTTPStatus.NOT_FOUND, 'Ресурс не доступен, код ответа 404. Проверь *urls.py*.'

        assert (
            response.context_data['view'].template_name == 'accounts/signup.html'
        ), 'Ошибка!! Класс SignupView не использует шаблон `account/signup.html'
        assert 'form' in response.context_data, 'В контекст не передан объект формы.'
        assert 'email' in response.context_data['form'].fields, 'В форме нет поля `email`, проверь *forms.py*.'
        assert 'password1' in response.context_data['form'].fields, 'В форме нет поля `password1`, проверь *forms.py*.'
        assert 'password2' in response.context_data['form'].fields, 'В форме нет поля `password2`, проверь *forms.py*.'
        assert (
            response.context_data['form'].fields['email'].required
        ), 'Проверь что поле `email` обязательно для заполнения.'
        assert (
            response.context_data['form'].fields['password1'].required
        ), 'Проверь что поле `password1` обязательно для заполнения.'
        assert (
            response.context_data['form'].fields['password2'].required
        ), 'Проверь что поле `password2` обязательно для заполнения.'

    @pytest.mark.django_db(transaction=True)
    def test_valid_user_signup(self, client, django_user_model):
        response = client.post(
            TestSignup.SIGNUP_URL,
            data=TestSignup.VALID_DATA,
            headers={'HX-Request': 'true'},
        )

        assert response.status_code == HTTPStatus.SEE_OTHER, 'Корректный запрос должен возвращать код 303'
        new_user = django_user_model.objects.filter(email=TestSignup.VALID_DATA['email'])

        assert new_user.exists(), 'Корректный запрос не создаёт нового пользователя.'

        assert not new_user[0].is_active, 'Созданный аккаунт не требует подтверждения.'

        new_user.delete()

    @pytest.mark.django_db(transaction=True)
    def test_invalid_user_signup(self, client, django_user_model):
        invalid_data = {
            'email': 'tes@^^tuser.mail.com',
            'password': '',
        }
        users_number = django_user_model.objects.count()
        response = client.post(
            TestSignup.SIGNUP_URL,
            data=invalid_data,
            headers={'HX-Request': 'true'},
        )

        assert response.status_code != HTTPStatus.FOUND, 'При отправке некоректных данных не возвращается код 302'
        assert (
            django_user_model.objects.count() == users_number
        ), 'При отправке не коректных данных создатся пользователь.'

    @pytest.mark.django_db(transaction=True)
    def test_send_confirm_code(self, client):
        session = client.session
        session['user_email'] = 'testuser@email.com'
        session.save()
        outbox_before_count = len(mail.outbox)
        client.get(
            TestSignup.CONFIRM_SIGNUP_URL,
            headers={'HX-Request': 'true'},
        )
        outbox_after = mail.outbox

        assert (
            len(outbox_after) == outbox_before_count + 1
        ), 'При корректном запросе не отправляется письмо с кодом подтверждения.'

        assert (
            client.session['user_email'] in outbox_after[0].to
        ), 'Если отправлен корректный запрос - письмо должно быть отправленно на правильный адрес'

    @pytest.mark.django_db(transaction=True)
    def test_confirm_signup(self, client, django_user_model):
        django_user_model.objects.create_user(email='testuser@email.com', password='secret')
        session = client.session
        session['confirm_code'] = '1111'
        session['user_email'] = 'testuser@email.com'
        session.save()
        response = client.post(
            TestSignup.CONFIRM_SIGNUP_URL,
            data={'num1': '1', 'num2': '1', 'num3': '1', 'num4': '1'},
            headers={'HX-Request': 'true'},
        )

        assert (
            response.status_code == HTTPStatus.SEE_OTHER
        ), 'После успешного подтверждения аккаунта пользователь не перенаправляется на страницу входа.'
        assert django_user_model.objects.get(
            email='testuser@email.com',
        ).is_active, 'При вводе коректных данных аккаунт не становится активным.'


class TestSignin:
    SIGNIN_URL = reverse_lazy('accounts:signin')

    def test_non_htmx_request(self, client):
        response = client.get(TestSignin.SIGNIN_URL)
        assert (
            response.status_code == HTTPStatus.FORBIDDEN
        ), 'Пользователь имеет досту к служебному ресурсу `accounts/signin/`, проверь *views.py*.'

        response = client.post(TestSignin.SIGNIN_URL)
        assert (
            response.status_code == HTTPStatus.FORBIDDEN
        ), 'Пользователь имеет досту к служебному ресурсу `accounts/signin/, проверь *views.py*.'

    def test_nodata_signin(self, client):
        empty_response = client.post(
            TestSignin.SIGNIN_URL,
            headers={'HX-Request': 'true'},
        )
        assert (
            'email' in empty_response.context_data['form'].errors
        ), 'Форма не передаёт информацию об ошибках в поле `email`'
        assert (
            'password' in empty_response.context_data['form'].errors
        ), 'Форма не передаёт информацию об ошибках в поле `password`'

    @pytest.mark.django_db(transaction=True)
    def test_ivalid_data_signin(self, client, django_user_model):
        user = django_user_model.objects.create_user(email='usertest@emal.com', password='secret')
        not_active_signin = client.post(
            TestSignin.SIGNIN_URL,
            data={
                'email': user.email,
                'password': 'secret',
            },
            headers={'HX-Request': 'true'},
        )
        assert (
            not_active_signin.status_code != HTTPStatus.FOUND
        ), 'Пользователь входит в сисему с не правильными данными.'
        assert (
            '__all__' in not_active_signin.context_data['form'].errors
        ), 'Пользователь не видит сообщение о том что его аккаунт не активен.'
        user.is_active
        user.save()

        invalid_data_signin = client.post(
            TestSignin.SIGNIN_URL,
            data={
                'email': user.email,
                'password': 'wrong_password',
            },
            headers={'HX-Request': 'true'},
        )
        assert (
            not_active_signin.status_code != HTTPStatus.FOUND
        ), 'Пользователь входит в сисему с не правильными данными.'
        assert (
            '__all__' in invalid_data_signin.context_data['form'].errors
        ), 'Пользователь не видит сообщение о том что введены не правильные данные'

    def test_signin_context(self, client):
        response = client.get(TestSignin.SIGNIN_URL, headers={'HX-Request': 'true'})

        assert response.status_code != HTTPStatus.NOT_FOUND, 'Ресурс не доступен, код ответа 404. Проверь *urls.py*.'
        assert response.status_code == HTTPStatus.OK, f'Ресурс не доступен, код ответа {response.status_code }.'
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
            'password': 'secret',
        }
        user = django_user_model.objects.create_user(**valid_data)
        user.is_active = True
        user.save()

        response = client.post(
            TestSignin.SIGNIN_URL,
            data=valid_data,
            headers={'HX-Request': 'true'},
        )

        assert response.status_code != HTTPStatus.NOT_FOUND, 'Ресурс `accounts/signin/` не найден, проверь *urls.py*.'
        assert response.status_code == HTTPStatus.OK, 'Корректный запрос не возвращает код 302.'
        assert (
            response.wsgi_request.user.is_authenticated
        ), 'При отправке корректных данных пользователь не был авторизован.'
        user.delete()


class TestLogout:
    LOGOUT_URL = reverse_lazy('accounts:logout')

    def test_valid_request(self, client, django_user_model):
        valid_data = {
            'email': 'testuser@mail.com',
            'password': 'secret',
        }
        user = django_user_model.objects.create(**valid_data)
        client.force_login(user)
        response = client.post(TestLogout.LOGOUT_URL)

        assert response.status_code != HTTPStatus.NOT_FOUND, 'Ресурс `accounts/logout/` не найден, проверь *urls.py*.'
        assert response.status_code == HTTPStatus.FOUND, 'Корректный запрос возвращает код 302.'
        assert response.wsgi_request.user.is_anonymous, 'При корректном запросе пользователь не вышел из системы.'
