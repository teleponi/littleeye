from django.db import models
from django.core.validators import MaxValueValidator


class ItemType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Order(models.Model):

    class OrderType(models.TextChoices):
        INLINE = "inline"
        OFFLINE = "offline"

    name = models.CharField(max_length=100)
    ordertype = models.CharField(max_length=20,
                                 choices=OrderType.choices)
    price = models.FloatField(
        help_text="nur positive Zahlen",
        validators=[MaxValueValidator(1120)])
    item_type = models.ForeignKey(ItemType, on_delete=models.CASCADE,
                                  related_name="orders", blank=True, null=True)

    def __str__(self) -> str:
        return self.name
