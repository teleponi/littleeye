import logging

from django.forms.models import model_to_dict
from django.test import TestCase
from django.core.exceptions import ValidationError
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


class TicketModelTests(TestCase):
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

    def test_invalid_ticket_name_too_short(self):
        """ticket name must be greaterequal 3 chars"""

        self.ticket.name = "aa"
        self.assertRaises(ValidationError, self.ticket.full_clean)

    def test_invalid_ticket_name_too_long(self):
        """ticket name must be smaller than 50 chars"""

        self.ticket.name = "a" * 51
        self.assertRaises(ValidationError, self.ticket.full_clean)

    def test_invalid_ticket_description_too_long(self):
        """ticket name must be smaller than 1200 chars"""

        self.ticket.description = "a" * 1201
        self.assertRaises(ValidationError, self.ticket.full_clean)

        """ticket name must be greaterequals 3 chars"""

        self.ticket.description = "aa"
        self.assertRaises(ValidationError, self.ticket.full_clean)

    def test_invalid_ticket_location_too_long(self):
        """ticket name must NOT be greaterequals 100 chars"""

        self.ticket.location = "a" * 101
        self.assertRaises(ValidationError, self.ticket.full_clean)


class CommentModelTests(TestCase):
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

        self.comment = Comment.objects.create(
            name="valid name",
            description="valid description",
            ticket=self.ticket,
            author=self.tutor,
        )

    def test_invalid_comment_name_too_short(self):
        """comment name must be greaterequal 3 chars"""

        self.comment.name = "a"
        self.assertRaises(ValidationError, self.comment.full_clean)

    def test_invalid_comment_name_too_long(self):
        """ticket name must be smaller than 50 chars"""

        self.comment.name = "a" * 51
        self.assertRaises(ValidationError, self.comment.full_clean)

    def test_invalid_comment_description_too_long(self):
        """comment descriptoin must be smaller than 1200 chars"""

        self.comment.description = "a" * 1201
        self.assertRaises(ValidationError, self.comment.full_clean)

    def test_invalid_comment_description_too_short(self):
        """comment name must be greaterequals 3 chars"""

        self.comment.description = "aa"
        self.assertRaises(ValidationError, self.comment.full_clean)
