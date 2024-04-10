from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    code = forms.CharField(
        label='Código de registro',
        help_text='Insira o código de registro previamente obtido.',
        required=True
    )

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', )