""" 
hier wird die User-Fabrik erstellt. Diese 
"""
import factory
from django.contrib.auth import get_user_model  # aktuelles User-Model
from django.contrib.auth.hashers import make_password


class UserFactory(factory.django.DjangoModelFactory):
    """
    factory boy stellt mit  DjangoModelFactory eine Möglichkeit zur 
    Verfügung, eine Django-Model Instanz zu erstellen
    """
    class Meta:
        model = get_user_model()

    username = factory.Faker("user_name")
    email = factory.Faker("email")
    password = factory.LazyFunction(
        lambda: make_password("abc")
    )
