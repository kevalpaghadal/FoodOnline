from typing import Any
from django import forms
from .models import user

class userform(forms.ModelForm):
    # add custom fields
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = user
        fields  = ['first_name' , 'last_name', 'username' , 'email' , 'password']

    # compare password and confirm password
    def clean(self):
        cleaned_data = super(userform , self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError('password does not match')