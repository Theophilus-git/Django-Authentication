from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirmed')

        # Checking if passwords matches
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Password does not match")   

        return cleaned_data 
