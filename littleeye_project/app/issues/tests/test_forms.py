import logging
from http import HTTPStatus

from django.forms.models import model_to_dict
from django.test import Client, TestCase
from unittest import skip
from django.urls import reverse

from issues.models import Ticket, MediaType, Status, Severity, Comment
from courses.models import Course
from user.factories import UserFactory
from user.models import Role


logging.disable(logging.CRITICAL)


def create_user(role: Role):
    user = UserFactory(role=role)
    return user


def create_course(tutor, name: str = "Mathe 1", shortcut: str = "m1") -> Course:
    return Course.objects.create(name=name, tutor=tutor, shortcut=shortcut)


def create_mediatypes(name: str = "Skript") -> MediaType:
    return MediaType.objects.create(name=name)


def create_ticket(**kwargs):
    return Ticket.objects.create(**kwargs)


class StudentTicketFormTests(TestCase):
    def setUp(self):
        self.tutor = create_user(role=Role.TUTOR)
        self.student = create_user(role=Role.STUDENT)
        self.course = create_course(self.tutor)
        self.ticket = create_ticket(
            name="error",
            description="some description",
            location="some location",
            media_type=create_mediatypes(name="Podcast"),
            course=self.course,
            author=create_user(role=Role.STUDENT),
        )

        self.client = Client()

        self.payload = {
            "name": "Fehler",
            "description": "Fehlertext",
            "location": "Ort des Fehlers",
            "media_type": create_mediatypes().pk,
            "course": create_course(self.tutor).pk,
        }

    def test_tutor_overview_accessible(self):
        """Can Tutor access overview page? Ticket 8"""
        self.client.force_login(self.tutor)

        res = self.client.get(reverse("issues:issues"))
        self.assertEquals(res.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(res, "issues/ticket_list.html")
        self.assertContains(res, text="Übersichtsseite")

    def test_tutor_overview_anonymously_not_accessible(self):
        """Can anonymous user access overview page?

        anonymous user should be redirected to login.
        Ticket 9
        """
        res = self.client.get(reverse("issues:issues"))
        self.assertEquals(res.status_code, HTTPStatus.FOUND)

    def test_student_cannot_close_ticket(self):
        """Student darf das Ticket nicht schließen, indem es auf erledigt gesetzt wird.
        ticket 1"""
        self.client.force_login(self.student)

        payload = model_to_dict(self.ticket)

        # das darf nicht passieren...
        payload["status"] = Status.COMPLETED
        res = self.client.post(
            reverse("issues:issue_update_tutor", args=(self.ticket.pk,)), payload
        )

        # Diese Aktion ist verboten für die Rolle Student
        self.assertEquals(res.status_code, HTTPStatus.FORBIDDEN)
        ticket = Ticket.objects.get(pk=self.ticket.pk)
        # status darf nicht verändert sein (initial ist Status.NEW == 0)
        self.assertEqual(ticket.status, Status.NEW)

    def test_student_cannot_edit_ticket(self):
        """Student darf ein Ticket nicht editieren. Ticket 2"""
        self.client.force_login(self.student)
        payload = model_to_dict(self.ticket)
        payload["status"] = Status.CLOSED

        res = self.client.get(
            reverse("issues:issue_update_tutor", args=(self.ticket.pk,))
        )
        self.assertEquals(res.status_code, HTTPStatus.FORBIDDEN)
        res = self.client.post(
            reverse("issues:issue_update_tutor", args=(self.ticket.pk,)), payload
        )
        self.assertEquals(res.status_code, HTTPStatus.FORBIDDEN)
        ticket = Ticket.objects.get(pk=self.ticket.pk)
        self.assertNotEqual(ticket.status, Status.CLOSED)

    def test_tutor_can_set_status_and_severity(self):
        """Tutor darf den Status und Schweregrad eines Tickets ändern.Ticket 5."""
        self.client.force_login(self.tutor)

        payload = model_to_dict(self.ticket)
        payload["status"] = Status.COMPLETED
        payload["severity"] = Severity.URGENT
        res = self.client.post(
            reverse("issues:issue_update_tutor", args=(self.ticket.pk,)), payload
        )
        self.assertEquals(res.status_code, HTTPStatus.FOUND)
        ticket = Ticket.objects.get(pk=self.ticket.pk)
        # Prototype: Wenn COMPLETED, dann setzen wir intern auf CLOSED
        self.assertEqual(ticket.status, Status.CLOSED)
        self.assertEqual(ticket.severity, Severity.URGENT)

    def test_tutor_can_close_ticket(self):
        """Tutor darf ein Ticket schließen, indem es auf erledigt gesetzt wird.
        ticket 7"""
        self.client.force_login(self.tutor)

        payload = model_to_dict(self.ticket)
        payload["status"] = Status.COMPLETED
        res = self.client.post(
            reverse("issues:issue_update_tutor", args=(self.ticket.pk,)), payload
        )
        self.assertEquals(res.status_code, HTTPStatus.FOUND)
        ticket = Ticket.objects.get(pk=self.ticket.pk)
        # Prototype: Wenn COMPLETED, dann setzen wir intern auf CLOSED
        self.assertEqual(ticket.status, Status.CLOSED)

    def test_ticket_tutor_not_created(self):
        """Ticket must not be created by Tutor. ticket 4"""
        self.client.force_login(self.tutor)

        res = self.client.post(
            reverse("issues:issue_create"),
            self.payload,
        )
        self.assertEquals(res.status_code, HTTPStatus.FORBIDDEN)
        tickets = Ticket.objects.filter(name=self.payload["name"])
        self.assertFalse(tickets.exists())

    def test_ticket_student_created(self):
        """Ticket can be created by Student. ticket 3"""
        self.client.force_login(self.student)

        res = self.client.post(
            reverse("issues:issue_create"),
            self.payload,
        )
        self.assertEquals(res.status_code, HTTPStatus.FOUND)
        tickets = Ticket.objects.filter(name=self.payload["name"])
        self.assertTrue(tickets.exists())


class CommentFormTests(TestCase):
    def setUp(self):
        self.tutor = create_user(role=Role.TUTOR)
        self.student = create_user(role=Role.STUDENT)
        self.course = create_course(self.tutor)
        self.ticket = create_ticket(
            name="error",
            description="some description",
            location="some location",
            media_type=create_mediatypes(name="Podcast"),
            course=self.course,
            author=create_user(role=Role.STUDENT),
        )

        self.client = Client()

        self.payload = {
            "name": "valid title",
            "description": "valid comment",
        }

    def test_tutor_can_create_comment(self):
        """Can Tutor can create a comment for a ticket? ticket 6"""
        self.client.force_login(self.tutor)

        res = self.client.get(reverse("issues:comment_create", args=(self.ticket.pk,)))
        self.assertEquals(res.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(res, "issues/comment_form.html")

        res = self.client.post(
            reverse("issues:comment_create", args=(self.ticket.pk,)), self.payload
        )
        self.assertEquals(res.status_code, HTTPStatus.FOUND)
        comment = Comment.objects.filter(name=self.payload["name"])
        self.assertTrue(comment.exists())

    def test_student_cannot_create_comment(self):
        """Student can not set up a comment. ticket 10"""
        self.client.force_login(self.student)

        res = self.client.get(reverse("issues:comment_create", args=(self.ticket.pk,)))
        self.assertEquals(res.status_code, HTTPStatus.FORBIDDEN)

        res = self.client.post(
            reverse("issues:comment_create", args=(self.ticket.pk,)), self.payload
        )
        self.assertEquals(res.status_code, HTTPStatus.FORBIDDEN)
        comment = Comment.objects.filter(name=self.payload["name"])
        self.assertFalse(comment.exists())
