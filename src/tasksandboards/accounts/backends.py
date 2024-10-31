from django.contrib.auth import get_user_model
from django.shortcut import get_object_or_404

UserModel = get_user_model()


class EmailBackend:
    def authenticate(self, request, email=None, password=None, **kwargs):
        if email is None:
            email = kwargs.get(UserModel.EMAIL_FIELD)
        if email is None or password is None:
            return None
        try:
            user = get_object_or_404(UserModel, email=email)
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

        def get_user(self, user_id):
            try:
                user = UserModel._default_manager.get(pk=user_id)
            except UserModel.DoesNotExist:
                return None
            return user if self.user_can_authenticate(user) else None
