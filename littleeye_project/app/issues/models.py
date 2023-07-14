from django.db import models
from django.db.models.fields import related
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from courses.models import Course
from .managers import EnhancedManager, IssueQuerySet

User = get_user_model()


class Status(models.IntegerChoices):
    IN_PROGRESS = 1, "in Bearbeitung"
    CLOSED = 2, "geschlossen"
    RE_OPENED = 3, "wiedergeöffnet"


class Severity(models.IntegerChoices):
    MINOR = 1, "unbedeutend"
    NORMAL = 2, "normal"
    URGENT = 3, "dringend"
    LARGE = 4, "sofort"


class DateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(models.Model):
    icon = models.CharField(max_length=19, null=True, blank=True)
    name = models.CharField(
        max_length=99,
        unique=True,
    )
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class MediaType(models.Model):
    """Der Medientyp eines Issues."""

    name = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(3), MaxLengthValidator(50)],
    )
    icon = models.CharField(max_length=19, null=True, blank=True)

    def __str__(self):
        return self.name


class Issue(DateMixin):
    """Repräsentiert einen Issue.

    related to :model:`issues.MediaType` and :model:`user.User`.
    """

    updated_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="iusses"
    )
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3, message="Custom")],
    )
    location = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3)],
        blank=True,
        null=True,
        help_text="Wo ist der Fehler aufgetreten? Zeile, Minute, Seite, ect.",
    )
    description = models.TextField(validators=[])
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name="issues")
    severity = models.IntegerField(choices=Severity.choices)
    status = models.IntegerField(choices=Status.choices, default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="issues")
    media_type = models.ForeignKey(
        MediaType, on_delete=models.PROTECT, related_name="issues"
    )
    tags = models.ManyToManyField(Tag, related_name="issues", blank=True)
    objects = EnhancedManager.from_queryset(IssueQuerySet)()

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["author", "name"], name="unique_author"),
        ]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("issues:issue_detail", kwargs={"pk": str(self.pk)})


class IssueHistory(DateMixin):
    """Der Lebenszyklus eines Issues in der History-Tabelle.

    related to :model:`issues.Issue` and :model:`user.User`.
    """

    class Type(models.IntegerChoices):
        ISSUE_CREATED = 1, "Ticket wurde erstellt"
        STATUS_CHANGED = 2, "Status wurde geändert"
        COMMENT_ADDED = 3, "Kommentar wurde hinzugefügt"
        ISSUE_CLOSED = 4, "Ticket wurde geschlossen"

    type = models.IntegerField(choices=Type.choices)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="history")
    status = models.IntegerField(choices=Status.choices)
    severity = models.IntegerField(choices=Severity.choices)
    updated_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="history"
    )

    def __str__(self):
        return f"{self.issue}-{self.status}"


class Comment(DateMixin):
    """Ein Kommentar zu einem Ticket.

    related to :model:`issues.Issue` and :model:`user.User`.
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(
                3, message="der Titel muss mindestens drei Zeichen lang sein!"
            )
        ],
    )
    description = models.TextField(validators=[])
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="comments")
