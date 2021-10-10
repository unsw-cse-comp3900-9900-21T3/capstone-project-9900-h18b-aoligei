from django import forms
from User.models import User

from django.contrib.auth.models import User

class UserLoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )

class UserRegisterForm(forms.ModelForm):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email',
        )

