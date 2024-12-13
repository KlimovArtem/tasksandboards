from django.urls import reverse_lazy
import pytest


class TestCreateBoard:
    CREATE_BOARD_URL = reverse_lazy('boards:create')

    def test_create_board_url_accsses(self, client, django_user_model):
        unauthorize_response = client.get(self.CREATE_BOARD_URL)

        assert unauthorize_response.status != 200, "Не авторизованный пользователь имеет доступ к ресурсу."
        assert unauthorize_response.status == 302, "Не авторизованный пользователь не перенаправляется на страницу авторизации."