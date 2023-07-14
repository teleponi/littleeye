from typing import List
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
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
from .models import Issue, Comment, IssueHistory, Status, Severity
from .forms import StudentIssueForm, TutorIssueForm, CommentForm


class UserIsCourseTutor(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().course.tutor == self.request.user


class UserIsOwner(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user


class IssueHistoryListView(ListView):
    model = IssueHistory

    def get_queryset(self) -> QuerySet:
        self.issue = get_object_or_404(Issue, pk=self.kwargs["issue_id"])
        queryset = IssueHistory.objects.filter(issue=self.issue)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["issue"] = self.issue
        return ctx


def create_history(type_, issue, status, severity, updated_by):
    history = IssueHistory(
        type=type_, issue=issue, status=status, severity=severity, updated_by=updated_by
    )
    history.save()


class CommentCreateView(SuccessMessageMixin, CreateView):
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

        create_history(
            type_=IssueHistory.Type.COMMENT_ADDED,
            issue=issue,
            status=issue.status,
            severity=issue.severity,
            updated_by=form.instance.author,
        )
        return response

    def get_initial(self):
        self.issue = get_object_or_404(Issue, pk=self.kwargs["issue_id"])

    def get_success_url(self):
        return reverse("issues:issue_detail_tutor", args=(self.object.issue.pk,))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["object"] = self.issue
        return ctx


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
        form.instance.status = 0
        form.instance.severity = 1
        form.instance.updated_by = self.request.user
        response = super().form_valid(form)

        create_history(
            type_=IssueHistory.Type.ISSUE_CREATED,
            issue=form.instance,
            status=form.instance.status,
            severity=form.instance.severity,
            updated_by=form.instance.author,
        )
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
    queryset = Issue.objects.all()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["toggle_active"] = self.request.GET.get("inactive") == "true"
        return ctx

    def get_queryset(self):
        show_closed = self.request.GET.get("inactive") == "true"
        qs = super().get_queryset()
        if self.request.user.role == "TUTOR":
            return qs.tutor(self.request.user).active(show_closed=show_closed)
        return qs.author(self.request.user).active(show_closed=show_closed)


class IssueUpdateTutorView(UserIsCourseTutor, SuccessMessageMixin, UpdateView):
    """
    issue/update/3
    """

    model = Issue
    form_class = TutorIssueForm
    success_message = "Ticket wurde erfolgreich aktualisiert"
    template_name = "issues/issue_form_tutor.html"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        if form.has_changed():
            print("The following fields changed: %s" % ", ".join(form.changed_data))
            create_history(
                type_=IssueHistory.Type.STATUS_CHANGED,
                issue=form.instance,
                status=form.instance.status,
                severity=form.instance.severity,
                updated_by=self.request.user,
            )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("issues:issue_detail_tutor", args=(self.object.pk,))


class IssueDetailTutorView(UserIsCourseTutor, DetailView):
    """
    issue/slug-name
    """

    model = Issue
    template_name = "issues/issue_detail_tutor.html"
