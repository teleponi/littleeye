import logging
from http import HTTPStatus
from unittest import skip
from django.forms import Media

from django.forms.models import model_to_dict
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from issues.models import Ticket, MediaType, Status, Severity
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

    def test_student_form_accessible(self):
        """Is Student Form Accessbile for logged in student?"""
        self.client.force_login(self.student)
        res = self.client.get(reverse("issues:issue_create"))
        self.assertEquals(res.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(res, "issues/ticket_form.html")
        self.assertContains(res, text="Neues Ticket anlegen")

    def test_student_cannot_delete_ticket(self):
        """Student darf ein Ticket nicht löschen."""
        self.client.force_login(self.student)

        res = self.client.get(reverse("issues:issue_delete", args=(self.ticket.pk,)))
        self.assertEquals(res.status_code, HTTPStatus.FORBIDDEN)
        res = self.client.post(reverse("issues:issue_delete", args=(self.ticket.pk,)))
        self.assertEquals(res.status_code, HTTPStatus.FORBIDDEN)
        tickets = Ticket.objects.filter(name=self.ticket.name)
        self.assertTrue(tickets.exists())

    def test_student_cannot_edit_ticket(self):
        """Student darf ein Ticket nicht editieren."""
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
        """Tutor darf den Status und Schweregrad eines Tickets ändern."""
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

    def test_student_form_not_accessible(self):
        """Is Student Form Accessbile for anonymous user?

        Redirect to login page (302)
        """
        res = self.client.get(reverse("issues:issue_create"))
        self.assertEquals(res.status_code, HTTPStatus.FOUND)

    def test_ticket_valid_created(self):
        """Was ticket with valid input data created in Database?"""
        self.client.force_login(self.student)

        res = self.client.post(
            reverse("issues:issue_create"),
            self.payload,
        )
        self.assertEquals(res.status_code, HTTPStatus.FOUND)
        tickets = Ticket.objects.filter(name=self.payload["name"])
        self.assertTrue(tickets.exists())

    def test_ticket_tutor_not_created(self):
        """Ticket must not be created by Tutor"""
        self.client.force_login(self.tutor)

        res = self.client.post(
            reverse("issues:issue_create"),
            self.payload,
        )
        self.assertEquals(res.status_code, HTTPStatus.FORBIDDEN)
        tickets = Ticket.objects.filter(name=self.payload["name"])
        self.assertFalse(tickets.exists())