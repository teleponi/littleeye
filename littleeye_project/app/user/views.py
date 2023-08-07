import logging

from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, reverse
from django.urls import reverse_lazy
from django.views import generic

from .forms import LoginForm, SignUpForm

logger = logging.getLogger(__name__)


class RedirectIfAuthenticatedMixin:
    def dispatch(self, request, *args, **kwargs):
        """wenn User schon eingeloggt, rediret zu start"""
        if self.request.user.is_authenticated:
            return redirect(reverse(self.redirect_to))
        return super().dispatch(request, *args, **kwargs)


class LoginView(auth_views.LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        """User bleibt auch nach Schließen des Browsers eingeloggt."""
        remember_me = form.cleaned_data["remember_me"]
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super().form_valid(form)


class SignUpView(RedirectIfAuthenticatedMixin, generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    redirect_to = "issues:issues"
