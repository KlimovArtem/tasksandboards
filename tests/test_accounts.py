import pytest
from django.test import Client


def test_accounts_login(client: Client) -> None:
    try:
        response = client.get('accounts/login/')
    except Exception as error:
        assert False, f"""Ресурс `accounts/login/` работает не коректно. Ошибка `{error}`."""

    assert (
        response.status_code == 200
    ), f'Ресурс не доступен, при запросе возвращается ответ с кодом {response.status_code }.'
    assert (
        response.status_code != 404
    ), 'Ресурс не доступен, при запросе возвращается ответ с кодом 404. Проверь *urls.py*.'
