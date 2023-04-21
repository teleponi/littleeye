from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from user.factories import UserFactory

User = get_user_model()


class Command(BaseCommand):
    """ 
    eigene Subkommandos erben immer von BaseCommand.
    """

    def add_arguments(self, parser) -> None:
        parser.add_argument("-n",
                            "--number",
                            type=int,
                            help="Number of Users to be generated",
                            required=True)

        parser.epilog = "Usage: python manage.py create_user -n 20"

    def handle(self, *args, **kwargs) -> None:
        n = kwargs.get("number")

        print("Deleting users...")
        User.objects.exclude(username="admin").delete()
        UserFactory.create_batch(n)
        print("Successfully created")
