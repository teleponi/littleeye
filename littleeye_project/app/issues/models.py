from django.db import models
from django.db.models.fields import related
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from courses.models import Course
from .managers import EnhancedManager, IssueQuerySet

User = get_user_model()


class Status(models.IntegerChoices):
    NEW = 0, "neu eingestellt"
    IN_PROGRESS = 1, "in Bearbeitung"
    COMPLETED = 2, "erledigt"
    CLOSED = 3, "geschlossen"


class Severity(models.IntegerChoices):
    NORMAL = 1, "normal"
    URGENT = 2, "dringend"
    LARGE = 3, "sofort"


class DateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(models.Model):
    name = models.CharField(
        max_length=99,
        unique=True,
    )

    def __str__(self):
        return self.name


class MediaType(models.Model):
    """Der Medientyp eines Issues."""

    name = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(3), MaxLengthValidator(50)],
    )

    def __str__(self):
        return self.name


class Ticket(DateMixin):
    """Repräsentiert einen Issue.

    related to :model:`issues.MediaType` and :model:`user.User`.
    """

    name = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(3)],
    )
    location = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3), MaxLengthValidator(100)],
        blank=True,
        null=True,
        help_text="Wo ist der Fehler aufgetreten? Zeile, Minute, Seite, ect.",
    )
    description = models.TextField(
        validators=[
            MinLengthValidator(3),
            MaxLengthValidator(1200),
        ],
    )
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name="tickets")
    severity = models.IntegerField(choices=Severity.choices, default=1)
    status = models.IntegerField(choices=Status.choices, default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    media_type = models.ForeignKey(
        MediaType, on_delete=models.PROTECT, related_name="tickets"
    )
    tags = models.ManyToManyField(Tag, related_name="tickets", blank=True)
    objects = EnhancedManager.from_queryset(IssueQuerySet)()

    class Meta:
        ordering = ["-severity", "status"]
        constraints = [
            models.UniqueConstraint(
                fields=["author", "name", "created_at"], name="unique_author"
            ),
        ]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("issues:issue_detail", kwargs={"pk": str(self.pk)})


class TicketHistory(DateMixin):
    """Der Lebenszyklus eines Issues in der History-Tabelle.

    related to :model:`issues.Issue` and :model:`user.User`.
    """

    class Type(models.IntegerChoices):
        TICKET_CREATED = 1, "Ticket wurde erstellt"
        STATUS_CHANGED = 2, "Status wurde geändert"
        COMMENT_ADDED = 3, "Kommentar wurde hinzugefügt"
        TICKET_CLOSED = 4, "Ticket wurde geschlossen"

    type = models.IntegerField(choices=Type.choices)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="history")
    comment = models.ForeignKey(
        "Comment",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="history",
    )
    status = models.IntegerField(choices=Status.choices)
    severity = models.IntegerField(choices=Severity.choices)
    updated_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="history"
    )

    def __str__(self):
        return f"{self.ticket}-{self.status}"


class Comment(DateMixin):
    """Ein Kommentar zu einem Ticket.

    related to :model:`issues.Issue`, :model:`user.User`.
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3),
            MaxLengthValidator(50),
        ],
    )
    description = models.TextField(
        validators=[
            MinLengthValidator(3),
            MaxLengthValidator(1200),
        ],
    )
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="comments"
    )

    def __str__(self) -> str:
        return self.name
