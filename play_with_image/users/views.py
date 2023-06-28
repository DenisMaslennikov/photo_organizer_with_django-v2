from django.views.generic import CreateView, UpdateView
from django.contrib.auth import views as auth_views, get_user_model
from django.urls import reverse, reverse_lazy

from .forms import LoginForm, NewUserForm, UserUpdateForm

Users = get_user_model()


class UserCreateView(CreateView):
    model = Users
    form_class = NewUserForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy("users:login")


class LoginView(auth_views.LoginView):
    form_class = LoginForm

    def get_success_url(self):
        if self.request.POST.get('next'):
            return self.request.POST.get('next')
        return reverse(
            'gallery:user_profile',
            args=(self.request.user.username, )
        )


class UserUpdateView(UpdateView):
    model = Users
    form_class = UserUpdateForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('users:edit_profile')

    def get_object(self, queryset=None):
        return self.request.user
