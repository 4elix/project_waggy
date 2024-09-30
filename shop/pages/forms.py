from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import ProductSize, ProductColor


class AddToCartForm(forms.Form):
    size = forms.ModelChoiceField(
        queryset=ProductSize.objects.none(),
        widget=forms.HiddenInput()
    )
    color = forms.ModelChoiceField(
        queryset=ProductColor.objects.none(),
        widget=forms.HiddenInput()
    )

    def __init__(self, product, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['size'].queryset = ProductSize.objects.filter(product=product)
        self.fields['color'].queryset = ProductColor.objects.filter(product=product)


class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mb-3 p-4',
        'placeholder': 'Your email address'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-3 p-4',
        'placeholder': 'Set your password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-3 p-4',
        'placeholder': 'Retype your password'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control mb-3 p-4',
        'placeholder': 'Your email address'
    }))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control mb-3 p-4',
        'placeholder': 'Enter username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control mb-3 p-4',
        'placeholder': 'Enter password'
    }))

    class Meta:
        model = User
        fields = ['username', 'password']
