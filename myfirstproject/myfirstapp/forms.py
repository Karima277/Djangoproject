from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import DateInput
from .models import CustomUser
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'username', 'birth_date', 'first_name', 'last_name']

        widgets = {
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
            'birth_date': DateInput(attrs={'type': 'date'}),
            'email': forms.TextInput(attrs={'placeholder': 'Enter your email'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter your Full name'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your Last name'}),
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

from django import forms
from .models import Promotion, Travel

class PromotionForm(forms.ModelForm):
    travel = forms.ModelChoiceField(queryset=Travel.objects.all(), label='Select Travel')

    class Meta:
        model = Promotion
        fields = ['name', 'discount_percentage', 'start_date', 'end_date', 'travel']

