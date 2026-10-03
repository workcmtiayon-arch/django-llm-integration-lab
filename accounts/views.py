from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import RegistrationForm


class RegistrationView(FormView):
    template_name = "accounts/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Your account has been created. Please sign in.")
        return super().form_valid(form)
