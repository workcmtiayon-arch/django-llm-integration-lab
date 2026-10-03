from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, UpdateView

from .forms import ProfilePhotoForm, ProfileUpdateForm, RegistrationForm


class RegistrationView(FormView):
    template_name = "accounts/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your account has been created. Please sign in.")
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfileUpdateForm
    template_name = "accounts/profile_edit.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated.")
        return super().form_valid(form)


class ProfilePhotoUpdateView(LoginRequiredMixin, UpdateView):
    form_class = ProfilePhotoForm
    template_name = "accounts/profile_photo_edit.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        old_photo = self.object.profile_photo
        response = super().form_valid(form)
        if old_photo and old_photo.name != self.object.profile_photo.name:
            old_photo.storage.delete(old_photo.name)
        messages.success(self.request, "Your profile photo has been updated.")
        return response
