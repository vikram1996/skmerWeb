from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

#form used to create a user
class skmerUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email')






