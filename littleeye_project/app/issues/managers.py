from django.db import models
from django.db.models import Count, Q


class IssueQuerySet(models.QuerySet):
    """Ein EventQueryset mit custom methods."""

    def tutor(self, user) -> models.QuerySet:
        return self.filter(course__tutor=user)

    def student(self) -> models.QuerySet:
        return self.filter(author__role="STUDENT")

    def active(self) -> models.QuerySet:
        """Filtert Queryset nach aktiven Objekten"""
        return self.filter(is_active=True)

    def author(self, author) -> models.QuerySet:
        return self.filter(author=author)

    def inactive(self) -> models.QuerySet:
        """Filtert Queryset nach inaktiven Objekten"""
        return self.filter(is_active=False)

    def search(self, query=None) -> models.QuerySet:
        if not query:
            return self.none()  # leeres Queryset

        return self.filter(models.Q(name__icontains=query))


class EnhancedManager(models.Manager):
    def get_queryset(self):
        return IssueQuerySet(self.model, using=self._db).prefetch_related(
            "author", "media_type", "tags"
        )
