from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

Users = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Имя пользователя",
        widget=forms.TextInput(attrs={"class": "form-control rounded-0"}),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control rounded-0"}),
    )


class NewUserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Users
        fields = ("username", "email", "first_name", "last_name")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ("username", "email", "first_name", "last_name")
