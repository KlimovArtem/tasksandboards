from django.urls import path

from accounts.views import LoginView, SigninView, SignupView, ConfirmSignupView


app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signin/', SigninView.as_view(), name='signin'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('confirm_signup', ConfirmSignupView.as_view(), name='confirm_signup'),
]
