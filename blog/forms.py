from django import forms
from .models import Application
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('name', 'surname', 'address', 'email')
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'birth_date', 'avatar']