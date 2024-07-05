from django import forms
from django.contrib.auth.models import User
from .models import *
class LoginForm(forms.Form):
    usuario = forms.CharField(
        max_length=150, 
        label='Usuario', 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Contraseña', 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match")

class ProductoForm(forms.ModelForm):
    class Meta:
        model = productos
        fields = ['name', 'categoria', 'precio', 'imagen', 'activate', 'destacado']
