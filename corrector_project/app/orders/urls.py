from django.urls import path
from django.views.generic.base import RedirectView

from . import views

app_name = "orders"

urlpatterns = [
    path("", RedirectView.as_view(url="order/create")),
    path(
        "order/create", views.OrderCreateView.as_view(), name="order_create"
    ),
    path(
        "order/update/<int:pk>",
        views.OrderUpdateView.as_view(),
        name="order_update",
    ),
    path(
        "order/delete/<int:pk>",
        views.OrderDeleteView.as_view(),
        name="order_delete",
    ),
]