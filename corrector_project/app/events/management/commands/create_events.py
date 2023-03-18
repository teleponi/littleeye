import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from events.models import Category, Event
from events.factories import CategoryFactory, EventFactory


class Command(BaseCommand):
    """ 
    eigene Subkommandos erben immer von BaseCommand.
    """

    def add_arguments(self, parser) -> None:
        parser.add_argument("-e",
                            "--events",
                            type=int,
                            help="Number of Events",
                            required=True)

        parser.add_argument("-c",
                            "--categories",
                            type=int,
                            help="Number of Categories",
                            required=True)

        parser.epilog = "Usage: python manage.py create_events -c 10 -e 200"

    def handle(self, *args, **kwargs) -> None:

        user_list = get_user_model().objects.all()
        if not user_list:
            print("es existieren keine User im System")
            raise SystemExit()

        for model in [Category, Event]:
            model.objects.all().delete()

        categories = CategoryFactory.create_batch(kwargs.get("categories"))

        for _ in range(kwargs.get("events")):
            EventFactory(
                category=random.choice(categories),
                author=random.choice(user_list)
            )
            # per random subtitle ja/nein
            # x.sub_title = None
            # x.save()
