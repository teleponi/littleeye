import random
import factory
import arrow
from django.utils import timezone
from user.factories import UserFactory
from . import models

categories = [
    "Sports",
    "Talk",
    "Cooking",
    "Freetime",
    "Hiking",
    "Movies",
    "Travelling",
    "Science",
    "Arts",
    "Pets",
    "Music",
    "Wellness",
    "Religion",
]


class CategoryFactory(factory.django.DjangoModelFactory):
    """Erstellt eine Kategorie aus einer Liste von 
    vorgefertigten Namen. Aufgrund des Iterators können
    wir nur maximal len(categories) Objekte anlegen.
    """
    class Meta:
        model = models.Category

    # Iterator nimmt immer den nächsten aus der Sequenz
    name = factory.Iterator(categories)
    sub_title = factory.Faker("sentence", locale="de_DE")

    # erstelle einen Absatz mit 20 Sätzen in de_DE
    description = factory.Faker("paragraph",
                                nb_sentences=20,
                                locale="de_DE")


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Event

    # die SubFactories benötigen wir in den Unit-Tests
    # falls nicht gegeben, nutze SubFactories
    category = factory.SubFactory(CategoryFactory)
    author = factory.SubFactory(UserFactory)

    name = factory.Faker("sentence", locale="de_DE")

    sub_title = factory.Faker("sentence", locale="de_DE")
    description = factory.Faker("paragraph",
                                nb_sentences=20,
                                locale="de_DE")
    min_group = factory.LazyAttribute(
        lambda _: random.choice(list(models.Event.Group))
    )

    date = factory.Faker(
        "date_time_between",
        start_date=arrow.utcnow().shift(days=1).datetime,
        end_date=arrow.utcnow().shift(days=100).datetime,
        tzinfo=timezone.get_current_timezone()
    )
    is_active = factory.LazyAttribute(
        lambda _: random.choice([True, False])
    )


# EventFactory(category=books)
