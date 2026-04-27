from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django.views.generic.edit import CreateView

from django.conf import settings
from .forms import CustomUserCreationForm, ProfileUserUpdateForm
from .models import CustomUser


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_mail(user.email)
        return super().form_valid(form)

    def send_welcome_mail(self, user_email):
        subject = "Добро пожаловать на сайт"
        message = "Спасибо, что зарегистрировались"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)


class ProfileUserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileUserUpdateForm
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("users:profile_user")

    def get_object(self, queryset=None):
        return self.request.user


class ProfileUserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/profile_user.html"
    success_url = reverse_lazy("users:profile_user")

    def get_object(self, queryset=None):
        return self.request.user
