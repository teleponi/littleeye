"""
PROJEKT URLS
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings

urlpatterns = [
    # http://127.0.0.1:8000/events/hello
    path("accounts/", include("user.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("", include("issues.urls")),
    # path("", RedirectView.as_view(url="events/categories")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
