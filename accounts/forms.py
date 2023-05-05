from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth import authenticate
from django.db import transaction


class UserRegister(UserCreationForm):
    email = forms.EmailField(max_length=50,help_text='Enter a valid Email')
    class Meta:
        model = User
        fields = ['first_name','last_name', 'email', 'password1','password2']



class UserAccountAuthenticationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")

    def clean_email(self):
        return self.cleaned_data['email'].lower()
