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
from .models import Ticket, Comment, TicketHistory, Status, Severity
from .forms import StudentTicketForm, TutorTicketForm, CommentForm


class UserIsCourseTutor(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().course.tutor == self.request.user


class UserIsOwner(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user


class IssueHistoryListView(ListView):
    model = TicketHistory

    def get_queryset(self) -> QuerySet:
        self.issue = get_object_or_404(Ticket, pk=self.kwargs["issue_id"])
        queryset = TicketHistory.objects.filter(ticket=self.issue)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["issue"] = self.issue
        return ctx


def create_history(type_, issue, status, severity, updated_by):
    history = TicketHistory(
        type=type_,
        ticket=issue,
        status=status,
        severity=severity,
        updated_by=updated_by,
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
        form.instance.ticket = self.ticket
        response = super().form_valid(form)

        ticket = Ticket.objects.get(pk=self.ticket.pk)

        create_history(
            type_=TicketHistory.Type.COMMENT_ADDED,
            issue=ticket,
            status=ticket.status,
            severity=ticket.severity,
            updated_by=form.instance.author,
        )
        return response

    def get_initial(self):
        self.ticket = get_object_or_404(Ticket, pk=self.kwargs["issue_id"])

    def get_success_url(self):
        return reverse("issues:issue_detail_tutor", args=(self.object.ticket.pk,))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["object"] = self.ticket
        return ctx


class IssueDeleteView(UserIsOwner, DeleteView):
    """
    issue/delete/3
    """

    model = Ticket


class IssueCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
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
        print("i am in initially detail view")


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
            print("The following fields changed: %s" % ", ".join(form.changed_data))

            # for the sake of the prototype
            # set ticket to CLOSED, if is set to COMPLETED
            print(form.instance.status, Status.COMPLETED)
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
