from django import forms
from django.contrib.auth.forms import UserCreationForm
from userprofile.models import Userprofile
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
#ceci est un form pour inscrire les differents utlisateurs ils contient differents champs comme le nom , prenom , email , password, photo..#
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    phone_number = forms.CharField(max_length=30, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'phone_number', 'profile_picture')
