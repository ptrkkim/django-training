from django import forms
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm

from src.core_auth.models import User


class UserCreationForm(DjangoUserCreationForm):

    class Meta:
        model = User
        fields = ("email",)
        field_classes = {'email': forms.EmailField}
