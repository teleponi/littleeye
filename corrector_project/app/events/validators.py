""" 
Zwei MÖglichkeiten, Validatoren zu erstellen.
1.) funktionsbasiert(!) a) ohne Parameter, b) mit Parameter
2.) Klasse

"""
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils import timezone
from collections.abc import Callable


def datetime_in_future(value) -> None:
    """löst einen ValidationError aus, wenn Zeitpunkt in der
    Vergangenheit liegt.
    value = aktueller Feldwert
    """
    if value < timezone.now():
        raise ValidationError("Der Zeitpunkt darf nicht in der Vergangenheit liegen!")


# def bad_word_validator(bad_word_list: list[str]) -> Callable:
# """
# als Closure definiert.
# """
# def inner(field_value) -> None:
# for word in bad_word_list:
# if word in field_value:
# raise ValidationError(
# "Dieses Wort ist nicht erlaubt!")
# return inner


@deconstructible
class BadWords:
    def __init__(self, words):
        self.bad_words = words

    def __call__(self, field_value) -> None:
        for word in self.bad_words:
            if word in field_value:
                raise ValidationError("Dieses Wort ist nicht erlaubt!")
