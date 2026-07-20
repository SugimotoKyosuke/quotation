from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .login_form import *


class LoginForm(AuthenticationForm):

    username = forms.CharField(
        label='ユーザー名',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'ユーザー名'
            }
        )
    )

    password = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control pe-5',
                'placeholder': 'パスワード'
            }
        )
    )