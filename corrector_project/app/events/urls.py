""" 
APP URLs
"""

from django.urls import path
from . import views

app_name = "events"

urlpatterns = [
    # http://127.0.0.1:8000/events/hello
    path("hello", views.hello_world, name="hello_world"),

    # http://127.0.0.1:8000/events/categories
    path("categories", views.categories, name="categories"),

    # http://127.0.0.1:8000/events/category/3
    path("category/<int:pk>", views.category, name="category_detail"),

    # http://127.0.0.1:8000/events/category/add
    path("category/add", views.category_add, name="category_add"),

    # http://127.0.0.1:8000/events/category/3/update
    path("category/<int:pk>/update",
         views.category_update,
         name="category_update"),

    # x = views.category_update
    # x(request, pk)

    # http://127.0.0.1:8000/events/event/add
    path("event/add",
         views.EventCreateView.as_view(),
         name="event_add"),

     # http://127.0.0.1:8000/events/event/3
     path("event/<int:pk>",
          views.EventDetailView.as_view(),
          name="event_detail"),
     
     # http://127.0.0.1:8000/events/event/3/delete
     path("event/<int:pk>/delete",
          views.EventDeleteView.as_view(),
          name="event_delete"),

     # http://127.0.0.1:8000/events
     path("",
          views.EventListView.as_view(),
          name="events"),
     
     # http://127.0.0.1:8000/events/search?q=suchwort
     path("search",
          views.EventSearchView.as_view(),
          name="events_search"),

     # http://127.0.0.1:8000/events/active
     path("active",
          views.ActiveEventsListView.as_view(),
          name="events_active"),
]
