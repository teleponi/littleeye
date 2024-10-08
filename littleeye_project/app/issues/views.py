from typing import List
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
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
from user.models import Role
from .models import Ticket, Comment, TicketHistory, Status, Severity
from .forms import StudentTicketForm, TutorTicketForm, CommentForm


class UserIsCourseTutor(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().course.tutor == self.request.user


class UserIsOwner(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user


class IsAdminUser(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class IsStudent(UserPassesTestMixin):
    def test_func(self):
        try:
            return self.request.user.role == Role.STUDENT
        except AttributeError:
            return False


class IssueHistoryListView(UserPassesTestMixin, ListView):
    model = TicketHistory

    def test_func(self):
        conditions = [
            self.request.user == self.issue.author,
            self.request.user == self.issue.course.tutor,
        ]
        if any(conditions):
            return True
        return False

    def dispatch(self, *args, **kwargs):
        self.issue = get_object_or_404(Ticket, pk=self.kwargs["issue_id"])
        return super().dispatch(*args, **kwargs)

    def get_queryset(self) -> QuerySet:
        queryset = TicketHistory.objects.filter(ticket=self.issue)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["ticket"] = self.issue
        return ctx


def create_history(type_, issue, status, severity, updated_by, comment=None):
    history = TicketHistory(
        type=type_,
        ticket=issue,
        status=status,
        severity=severity,
        updated_by=updated_by,
        comment=comment,
    )
    history.save()


class CommentDetailView(DetailView):
    """
    Kommentar wird im Modal auf der Ticket-History gezeigt.
    """

    model = Comment
    template_name = "issues/comment_detail_partial.html"


class CommentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    issue/3/comment
    """

    model = Comment
    success_message = "Kommentar wurde erfolgreich angelegt"
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.ticket = self.ticket
        response = super().form_valid(form)

        # ticket = Ticket.objects.get(pk=self.ticket.pk)

        create_history(
            type_=TicketHistory.Type.COMMENT_ADDED,
            issue=self.ticket,
            status=self.ticket.status,
            severity=self.ticket.severity,
            updated_by=form.instance.author,
            comment=form.instance,
        )
        return response

    def get_initial(self):
        self.ticket = get_object_or_404(Ticket, pk=self.kwargs["issue_id"])
        if self.request.user != self.ticket.course.tutor:
            raise PermissionDenied

    def get_success_url(self):
        return reverse("issues:issue_detail_tutor", args=(self.object.ticket.pk,))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["object"] = self.ticket
        return ctx


class IssueDeleteView(IsAdminUser, DeleteView):
    """
    issue/delete/3
    """

    model = Ticket


class IssueCreateView(IsStudent, SuccessMessageMixin, CreateView):
    """
    /issue/create
    """

    model = Ticket
    form_class = StudentTicketForm
    success_message = "Ticket wurde erfolgreich gemeldet"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 0
        form.instance.severity = 1
        form.instance.updated_by = self.request.user
        response = super().form_valid(form)

        create_history(
            type_=TicketHistory.Type.TICKET_CREATED,
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

    model = Ticket

    def get_initial(self):
        pass


class IssueListView(LoginRequiredMixin, ListView):
    """
    List all Tags by Name
    issues
    """

    model = Ticket
    queryset = Ticket.objects.all()

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

    model = Ticket
    form_class = TutorTicketForm
    success_message = "Ticket wurde erfolgreich aktualisiert"
    template_name = "issues/ticket_form_tutor.html"

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        if form.has_changed():
            # for the sake of the prototype
            # set ticket to CLOSED, if is set to COMPLETED
            if form.instance.status == Status.COMPLETED:
                form.instance.status = Status.CLOSED

            create_history(
                type_=TicketHistory.Type.STATUS_CHANGED,
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

    model = Ticket
    template_name = "issues/ticket_detail_tutor.html"
