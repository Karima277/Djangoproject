from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import DateInput
from .models import CustomUser
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'username', 'birth_date']
        widgets = {
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
            'birth_date': DateInput(attrs={'type': 'date'}),
            'email': forms.TextInput(attrs={'placeholder': 'Enter your email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter your Full name'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    class Meta:
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your email'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        }
# forms.py
