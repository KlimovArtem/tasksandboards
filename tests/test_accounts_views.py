from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from django.db.models import fields
from django.test import Client, RequestFactory

from tasksandboards.accounts.models import Account
from tasksandboards.accounts.views import SigninView, SignupView


class TestLogin:
    def test_login_url(self, client: Client):
        response = client.get("accounts/login/")
        assert (
            response.status_code == HTTPStatus.OK
        ), f"Ресурс не доступен, код ответа {response.status_code }."
        assert (
            response.status_code != HTTPStatus.NOT_FOUND
        ), "Ресурс не доступен, код ответа 404. Проверь *urls.py*."

    def test_login_view(self, client: Client):
        response = client.get("accounts/login/")
        assert (
            response.template == "accounts/login.html"
        ), "Ошибка!! Класс LoginView не использует шаблон `account/login.html"


class TestSignup:
    def test_signup_url_get(self, rf: RequestFactory, client: Client):
        htmx_request = rf.get("accounts/signup/")
        htmx_request.META["HX-Request"] = "true"
        htmx_response = SignupView.as_view()(htmx_request)
        response = client.get("accounts/signup/")

        assert (
            response.status_code == HTTPStatus.BAD_REQUEST
        ), "Пользователь имеет досту к служебному ресурсую, проверь *views.py*."
        assert (
            htmx_response.status_code == HTTPStatus.OK
        ), f"Ресурс не доступен, код ответа {htmx_response.status_code }."
        assert (
            htmx_response.status_code != HTTPStatus.NOT_FOUND
        ), "Ресурс не доступен, код ответа 404. Проверь *urls.py*."
        assert (
            htmx_response.template == "accounts/signup.html"
        ), "Ошибка!! Класс SignupView не использует шаблон `account/signup.html"
        assert "form" in htmx_response.context, "В контекст не передан объект формы."
        assert (
            "email" in htmx_response.context["form"].fields
        ), "В форме нет поля `email`, проверь *forms.py*."
        assert (
            "password" in htmx_response.context["form"].fields
        ), "В форме нет поля `password`, проверь *forms.py*."
        assert (
            "confirm_password" in htmx_response.context["form"].fields
        ), "В форме нет поля `confirm_password`, проверь *forms.py*."
        assert (
            htmx_response.context["form"].fields["email"].required
        ), "Проверь что поле `email` обязательно для заполнения."
        assert (
            htmx_response.context["form"].fields["password"].required
        ), "Проверь что поле `email` обязательно для заполнения."
        assert (
            htmx_response.context["form"].fields["confirm_password"].required
        ), "Проверь что поле `email` обязательно для заполнения."

    @pytest.mark.django_db(transaction=True)
    def test_signup_view_post(self, rf: RequestFactory):
        htmx_request = rf.post(
            "accounts/signup/",
            {
                "email": "testuser@email.com",
                "password": 1234567,
                "confirm_password": 1234567,
            },
        )
        htmx_request_wrong_data = rf.post(
            "accounts/signup/",
            {
                "email": "t@stuser@124email.com",
                "password": 1234567,
                "confirm_password": "1234567",
            },
        )
        htmx_request.META["HX-Request"] = "true"
        htmx_request_wrong_data.META["HX-Request"] = "true"
        htmx_response = SignupView.as_view()(htmx_request)
        response_with_wrong_data = SignupView.as_view()(htmx_request_wrong_data)

        assert Account.objects.filter(
            email="testuser@email.com",
        ).exists(), "Представление не создаёт объект в базе, проверь *views.py*."
        assert (
            htmx_response.status_code == HTTPStatus.SEE_OTHER
        ), "Пользователь не перенаправляется на страницу `accounts/login`, после регистрации."
        assert not Account.objects.filter(
            email="t@stuser@124email.com",
        ).exists(), "Представление создаёт объект в базе с не коректными данными, проверь *views.py*."
        assert (
            response_with_wrong_data.context["form"].fields["email"].errors
        ), "Форма не передаёт информацию об ошибках в поле `email`"
        assert (
            response_with_wrong_data.context["form"].fields["password"].errors
        ), "Форма не передаёт информацию об ошибках в поле `password`"
        assert (
            response_with_wrong_data.context["form"].fields["confirm_password"].errors
        ), "Форма не передаёт информацию об ошибках в поле `confirm_password`"


class TestSignin:
    def test_signin_get(self, rf: RequestFactory, client: Client):
        htmx_request = rf.get("accounts/signin/")
        htmx_request.META["HX-Request"] = "true"
        htmx_response = SigninView.as_view()(htmx_request)
        response = client.get("accounts/signin/")

        assert (
            response.status_code == HTTPStatus.BAD_REQUEST
        ), "Пользователь имеет досту к служебному ресурсую, проверь *views.py*."
        assert (
            htmx_response.status_code == HTTPStatus.OK
        ), f"Ресурс не доступен, код ответа {htmx_response.status_code }."
        assert (
            htmx_response.status_code != HTTPStatus.NOT_FOUND
        ), "Ресурс не доступен, код ответа 404. Проверь *urls.py*."
        assert (
            htmx_response.template == "accounts/signup.html"
        ), "Ошибка!! Класс SignupView не использует шаблон `account/signup.html"
        assert "form" in htmx_response.context, "В контекст не передан объект формы."
        assert (
            "email" in htmx_response.context["form"].fields
        ), "В форме нет поля `email`, проверь *forms.py*."
        assert (
            "password" in htmx_response.context["form"].fields
        ), "В форме нет поля `password`, проверь *forms.py*."
        assert (
            htmx_response.context["form"].fields["email"].required
        ), "Проверь что поле `email` обязательно для заполнения."
        assert (
            htmx_response.context["form"].fields["password"].required
        ), "Проверь что поле `email` обязательно для заполнения."

    @pytest.mark.django_db(transaction=True)
    def test_signin_view_post(self, rf: RequestFactory, client: Client):
        user = get_user_model().objects.create(
            email="testuser@email.com", password=1234567
        )
        htmx_request = rf.post(
            "accounts/signin/",
            {
                "email": "testuser@email.com",
                "password": 1234567,
            },
        )
        htmx_request_wrong_data = rf.post(
            "accounts/signin/",
            {
                "email": "t@stuser@124email.com",
                "password": 1234567,
            },
        )
        htmx_request.META["HX-Request"] = "true"
        htmx_request_wrong_data.META["HX-Request"] = "true"
        htmx_response = SignupView.as_view()(htmx_request)
        response_with_wrong_data = SignupView.as_view()(htmx_request_wrong_data)
        assert (
            htmx_response.status_code == HTTPStatus.SEE_OTHER
        ), "Пользователь не перенаправляется на запрашиваемую страницу."
        assert (
            user.is_authenticated
        ), "Пользователь не авторизовался, проверь *views.py*."
        assert (
            response_with_wrong_data.context["form"].fields["email"].errors
        ), "Форма не передаёт информацию об ошибках в поле `email`"
        assert (
            response_with_wrong_data.context["form"].fields["password"].errors
        ), "Форма не передаёт информацию об ошибках в поле `password`"


class TestAccountModel:
    def test_account_model(self):
        model_fields = Account._meta.fields
        email_field = next(field for field in model_fields if field.hasattr("email"))

        assert (
            email_field is not None
        ), "Модель `Account` должна содержать атрибут `email`."
        assert isinstance(
            email_field, fields.EmailField
        ), "Поле `email` должно быть типа `EmailField`"
        assert email_field.unique, "Поле `email` должно быть уникальным."
