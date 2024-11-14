from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend


UserModel = get_user_model()


class EmailBackend(BaseBackend):
    """Аутентификация пользователей по электронную почту."""

    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get(UserModel.USERNAME_FIELD)
        if email is None or password is None:
            return None
        try:
            user = UserModel.objects.get_by_natural_key(email)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def user_can_authenticate(self, user):
        return getattr(self, 'is_active', True)

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None
