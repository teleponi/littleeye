from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator

User = get_user_model()


class DateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(models.Model):
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=19)
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
    icon = models.CharField(max_length=19)


class Issue(DateMixin):
    """Repräsentiert einen Issue.

    related to :model:`issues.MediaType` and :model:`user.User`.
    """

    class Severity(models.IntegerChoices):
        MINOR = 1, "unbedeutend"
        NORMAL = 2, "normal"
        URGENT = 3, "dringend"
        LARGE = 4, "sofort"

    name = models.CharField(
        max_length=100,
        unique=True,
        validators=[MinLengthValidator(3, message="Custom")],
    )

    description = models.TextField(null=True, blank=True, validators=[])

    is_active = models.BooleanField(default=True)
    severity = models.IntegerField(choices=Severity.choices)

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="issues")
    media_type = models.ForeignKey(
        MediaType, on_delete=models.PROTECT, related_name="issues"
    )
    tags = models.ManyToManyField(Tag, related_name="issues", blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("eye:issue_detail", kwargs={"pk": str(self.pk)})