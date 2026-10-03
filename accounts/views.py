from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, UpdateView

from .forms import ProfilePhotoForm, ProfileUpdateForm, RegistrationForm

User = get_user_model()


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
        old_photo_name = User.objects.filter(pk=self.object.pk).values_list(
            "profile_photo", flat=True
        ).get()
        old_photo_storage = self.object.profile_photo.storage
        response = super().form_valid(form)
        if old_photo_name and old_photo_name != self.object.profile_photo.name:
            old_photo_storage.delete(old_photo_name)
        messages.success(self.request, "Your profile photo has been updated.")
        return response
