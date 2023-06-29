from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from .models import Issue
from .forms import IssueForm


class IssueDeleteView(DeleteView):
    """
    issue/delete/3
    """

    model = Issue


class IssueUpdateView(UpdateView):
    """
    issue/update/3
    """

    model = Issue
    form_class = IssueForm


class IssueCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    /issue/create
    """

    model = Issue
    form_class = IssueForm
    success_message = "Event wurde erfolgreich eingtragen"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class IssueListView(ListView):
    """
    List all Tags by Name
    issues
    """

    model = Issue


class IssueDetailView(DetailView):
    """
    issue/slug-name
    """

    model = Issue
