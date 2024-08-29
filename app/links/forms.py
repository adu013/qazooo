from typing import Any
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
        ]

    def clean(self):
        cleaned_data =  super().clean()
        return cleaned_data
