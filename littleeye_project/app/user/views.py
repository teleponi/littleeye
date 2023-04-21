import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, views as auth_views
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import FormView

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
        """remember me funktioniert nur, wennn alle instanzen des
        Browsers geschlossen werden"""
        remember_me = form.cleaned_data["remember_me"]
        if not remember_me:
            self.request.session.set_expiry(0)  # if remember me is
            self.request.session.modified = True
        return super().form_valid(form)


class SignUpView(RedirectIfAuthenticatedMixin, generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    redirect_to = "events:events"

    def form_valid(self, form):
        # response = super(SignUpView, self).form_valid(form)
        response = super().form_valid(form)
        # response ist ein HTTP-Redirect Object
        # <HttpResponseRedirect status_code=302, url="/user/login/">
        # würde auch gehen: return HttpResponseRedirect(self.get_success_url())
        try:
            user_group = Group.objects.get(name="Moderators")
            self.object.groups.add(user_group)

        except Group.DoesNotExist:
            logger.warning("Group in Signup View did not exist")
        return response
