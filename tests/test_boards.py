from django.urls import reverse_lazy
import pytest

from boards.models import Kanban


class TestCreateBoard:
    CREATE_BOARD_URL = reverse_lazy('boards:create')
    CREATE_KANBAN_URL = reverse_lazy('boards:create_kanban')

    @pytest.mark.django_db(transaction=True)
    def test_create_board_url_accsses(self, client, django_user_model):
        unauthorize_response = client.get(self.CREATE_BOARD_URL)

        assert (
            unauthorize_response.status_code != 404
        ), f'Ресурс `{self.CREATE_BOARD_URL}` не найден, проверь `urls.py`.'
        assert (
            unauthorize_response.status_code != 200
        ), f'Не авторизованный пользователь имеет доступ к ресурсу `{self.CREATE_BOARD_URL}`.'
        assert (
            unauthorize_response.status_code == 302
        ), 'Не авторизованный пользователь не перенаправляется на страницу авторизации.'
        assert (
            unauthorize_response['Location'] == reverse_lazy('accounts:login') + f'?next={self.CREATE_BOARD_URL}'
        ), 'Не авторизованный пользователь не перенаправляется на страницу авторизации.'

        user = django_user_model.objects.create_user('testuser@email.com', 'secret')
        client.force_login(user)
        authorize_response = client.get(self.CREATE_BOARD_URL)

        assert (
            authorize_response.status_code == 200
        ), f'Ресурс `{self.CREATE_BOARD_URL}` не доступен для авторизованного пользователя. Код ответа {authorize_response.status_code}.'

    @pytest.mark.django_db(transaction=True)
    def test_create_kanban_url_accsses(self, client, django_user_model):
        unauthorize_response = client.get(self.CREATE_KANBAN_URL)

        assert (
            unauthorize_response.status_code != 404
        ), f'Ресурс `{self.CREATE_KANBAN_URL}` не найден, проверь `urls.py`.'
        assert (
            unauthorize_response.status_code != 200
        ), f'Не авторизованный пользователь имеет доступ к ресурсу `{self.CREATE_KANBAN_URL}`.'
        assert (
            unauthorize_response.status_code == 302
        ), 'Не авторизованный пользователь не перенаправляется на страницу авторизации.'
        assert (
            unauthorize_response['Location'] ==  reverse_lazy('accounts:login') + f'?next={self.CREATE_KANBAN_URL}'
        ), 'Не авторизованный пользователь не перенаправляется на страницу авторизации.'

        user = django_user_model.objects.create_user('testuser@email.com', 'secret')
        client.force_login(user)
        authorize_response = client.get(self.CREATE_KANBAN_URL)

        assert (
            authorize_response.status_code == 200
        ), f'Ресурс `{self.CREATE_KANBAN_URL}` не доступен! Код ответа {authorize_response.status_code}.'

    @pytest.mark.django_db(transaction=True)
    def test_create_kanban_context(self, client, django_user_model):
        user = django_user_model.objects.create_user('testuser@email.com', 'secret')
        client.force_login(user)
        response = client.get(self.CREATE_KANBAN_URL)

        assert (
            response.context_data['view'].template_name == 'boards/create_kanban.html'
        ), 'Проверь `views.py` представление использует не правильный шаблон.'
        assert 'form' in response.context_data, 'В контекст не передан объект формы.'
        assert 'formset' in response.context_data, 'В контекст не передан объект набора форм колонок.'
        assert hasattr(response.context_data['formset'], 'management_form'
        ), 'В контекст не передан объект управленя набором форм.'
        assert (
            'TOTAL_FORMS' in response.context_data['formset'].management_form.fields
        ), 'В контекст не передана форма управления набора форм.'
        assert (
            'name' in response.context_data['form'].fields
        ), 'В объект формы не передаётся поле `name`.'
        assert (
            response.context_data['form'].fields['name'].required
        ), 'Поле `name` должно быть обязательным.'

    @pytest.mark.django_db(transaction=True)
    def test_invalid_create_kanban(self, client, django_user_model):
        board_owner = django_user_model.objects.create_user('testuser@email.com', 'secret')
        client.force_login(board_owner)
        existing_board = Kanban.objects.create(name='testname', owner=board_owner)
        start_numbers_of_boards = Kanban.objects.count()

        empty_data_response = client.post(self.CREATE_KANBAN_URL, data={})
        assert (
            empty_data_response.context_data['form'].errors
        ), 'При отправке пустого запроса в контекст не передаются сообщения об ошибках.'
        
        not_unique_data_response = client.post(self.CREATE_KANBAN_URL, data={'name': existing_board.name})
        assert (not_unique_data_response.context_data['form'].errors
        ), 'При отправке не уникальных данных в контекст не передаются сообщения об ошибках.'

        end_numbers_of_boards = Kanban.objects.count()
        assert (
            end_numbers_of_boards == start_numbers_of_boards
        ), 'При отправке не валидных данных создаётся доска.'
        
    @pytest.mark.django_db(transaction=True)
    def test_valid_create_kanban(self, client, django_user_model):
        board_owner = django_user_model.objects.create_user('testuser@email.com', 'secret')
        client.force_login(board_owner)
        start_numbers_of_boards = Kanban.objects.count()
        response = client.post(self.CREATE_KANBAN_URL, data={'name': 'testboard'})
        end_numbers_of_boards = Kanban.objects.count()
        assert response.status_code == 302, 'При успешной отправке форммы не происходит перенаправления'
        assert (
            response['Location'] == reverse_lazy('boards:board_content', kwrgs={'board_slug': 'testboard'})
        ), 'После успешного заполнения формы не происходит перенаправление на страницу с сожержимым доски'
        assert (
            end_numbers_of_boards != start_numbers_of_boards
        ), 'При отправке коректной формы не создайтся новая доска.'