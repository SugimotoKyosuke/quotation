from django.contrib.auth.views import LoginView, LogoutView

from base.forms import LoginForm


class UserLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm

class UserLogoutView(LogoutView):
    pass