from django.db import models

class ActiveManager(models.Manager):
    """ 
    ein Manager liefert eine Sub-Menge und wird 
    genutzt, wenn man diese Sub-Menge benötigt
    """
    def get_queryset(self):
        """Liefert die Submenge der aktiven Objekte."""
        qs = super().get_queryset()
        return qs.filter(is_active=True)