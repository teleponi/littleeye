import logging
from http import HTTPStatus
from unittest import skip

from django.contrib.auth.models import Group
from django.forms.models import model_to_dict
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from events.models import Issue
from user.factories import UserFactory


def create_moderators() -> Group:
    return Group.objects.create(name="moderatoren")


# https://www.valentinog.com/blog/testing-modelform/
def create_user(is_moderator: bool):
    user = UserFactory()
    if is_moderator:
        moderators_group = create_moderators()
        user.groups.add(moderators_group)
    return user


class EventFormTests(TestCase):
    # fixtures = ["events.json", "users.json"] VORSICHT, Geht hier nicht!
    # slug doppelt weil factory category schon vorhanden.

    def setUp(self):
        self.author = create_user(is_moderator=True)
        self.client = Client()
        self.client.force_login(self.author)
        self.cat = CategoryFactory()

        self.payload = {
            "name": "Seilspringen und Boxen",
            "description": "Spaß muss sein",
            "sub_title": "Seilspringen für Anfänger",
            "min_group": 10,
            "date": (timezone.now() + timedelta(days=2)),
            "is_active": True,
        }
        # "category": self.category.pk}

    def test_event_proper_update(self):
        """Test if update form works properly"""
        # self.event = EventFactory(author=self.author)
        self.event = EventFactory(author=self.author)  # sonst 404 Error
        # muss importiert werden: model_to_dict
        payload = model_to_dict(self.event)
        payload["name"] = "aaa"
        res = self.client.post(
            reverse("events:event_update", args=(self.event.pk,)), payload
        )
        self.assertEquals(res.status_code, HTTPStatus.FOUND)
        events = Event.objects.filter(name=payload["name"])
        self.assertTrue(events.exists())
