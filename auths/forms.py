from django import forms
from django.contrib.auth.forms import UserCreationForm


from auths.models import User


class ClientRegister(UserCreationForm):
    first_name = forms.CharField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, help_text='At least 8 characters.', label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, help_text='Confirm password.', label='Confirm password', )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')
