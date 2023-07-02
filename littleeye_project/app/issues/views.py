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
from .forms import StudentIssueForm


class UserIsCourseTutor(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().course.tutor == self.request.user


class UserIsOwner(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user


class IssueDeleteView(UserIsOwner, DeleteView):
    """
    issue/delete/3
    """

    model = Issue


class IssueCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    /issue/create
    """

    model = Issue
    form_class = StudentIssueForm
    success_message = "Event wurde erfolgreich eingtragen"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 1
        form.instance.severity = 1
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class IssueDetailView(UserIsOwner, DetailView):
    """
    issue/slug-name
    """

    model = Issue


class IssueListView(LoginRequiredMixin, ListView):
    """
    List all Tags by Name
    issues
    """

    model = Issue

    def get_queryset(self):
        if self.request.user.role == "TUTOR":
            return Issue.objects.tutor(self.request.user)
        return Issue.objects.author(self.request.user)


class IssueUpdateTutorView(UserIsCourseTutor, SuccessMessageMixin, UpdateView):
    """
    issue/update/3
    """

    model = Issue
    form_class = StudentIssueForm
    success_message = "Event wurde erfolgreich aktualisiert"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class IssueDetailTutorView(UserIsCourseTutor, DetailView):
    """
    issue/slug-name
    """

    model = Issue
    template_name = "issues/issue_detail_tutor.html"
