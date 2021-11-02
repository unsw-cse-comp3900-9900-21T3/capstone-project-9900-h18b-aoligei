from django import forms
from User.models import User,PersonalInfo
from django.db import models


from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = User
        fields = (
            'username',
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
class Personal_info_form(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = (

                  'firstname',
                  'lastname',
                  'gender',
                  'address',
                  'city',
                  'state',
                  'zipcode',
                  'country'
                  )


