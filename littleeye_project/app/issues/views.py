from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from .models import Issue, Comment, IssueHistory
from .forms import StudentIssueForm, TutorIssueForm, CommentForm


class UserIsCourseTutor(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().course.tutor == self.request.user


class UserIsOwner(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user


class CommentCreateView(CreateView):
    """
    issue/3/comment
    """

    model = Comment
    success_message = "Kommentar wurde erfolgreich angelegt"
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.issue = self.issue
        response = super().form_valid(form)

        issue = Issue.objects.get(pk=self.issue.pk)
        history = IssueHistory(
            type=3,
            issue=issue,
            status=issue.status,
            severity=issue.severity,
            updated_by=form.instance.author,
        )
        print("History:", history)
        history.save()
        return response

    def get_initial(self):
        self.issue = get_object_or_404(Issue, pk=self.kwargs["issue_id"])

    def get_success_url(self):
        return reverse("issues:issue_detail_tutor", args=(self.object.issue.pk,))


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
    success_message = "Ticket wurde erfolgreich gemeldet"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 1
        form.instance.severity = 1
        form.instance.updated_by = self.request.user
        response = super().form_valid(form)

        history = IssueHistory(
            type=1,
            issue=form.instance,
            status=form.instance.status,
            severity=form.instance.severity,
            updated_by=form.instance.author,
        )
        history.save()
        return response


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
    form_class = TutorIssueForm
    success_message = "Ticket wurde erfolgreich aktualisiert"
    template_name = "issues/issue_form_tutor.html"

    def form_valid(self, form):
        print(f"FORM DATA has changed: {form.has_changed()}")
        if form.has_changed():
            # hier ein History Objekt schreiben
            pass
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("issues:issue_detail_tutor", args=(self.object.pk,))


class IssueDetailTutorView(UserIsCourseTutor, DetailView):
    """
    issue/slug-name
    """

    model = Issue
    template_name = "issues/issue_detail_tutor.html"
