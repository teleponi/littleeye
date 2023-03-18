from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, HttpRequest, Http404
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Category, Event
from .service import ApiConsumer
from .forms import CategoryForm, EventForm


class EventDeleteView(LoginRequiredMixin, DeleteView):
    """
    http://127.0.0.1:8000/events/event/3/delete
    Template name: event_confirm_delete.html
    """
    model = Event
    success_url = reverse_lazy("events:events")


class ActiveEventsListView(ListView):
    """
    zeige hier nur aktive Events an.
    dazu überschreiben wir das QS.
    http://127.0.0.1:8000/events/active
    """
    model = Event
    queryset = Event.active_events.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["some_data"] = [1, 2, 3]
        return context


class EventSearchView(ListView):
    """ 
    http://127.0.0.1:8000/events/search?q=suchwort
    """
    model = Event

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "")
        
        return qs.filter(Q(name__icontains=q) | Q(sub_title__icontains=q))



class EventListView(ListView):
    """ 
    http://127.0.0.1:8000/events
    Template Name ist: MODELNAME_list.html
    generische Context-Name des Objekts ist: object_list

    default Queryset: Event.objects.all()
    """
    model = Event
    # template_name = "neues_template.html"
    # prefetch_related und select_related: Objekte vorladen

    # Reverse ForeignKey relationship (baut Django zusammen)
    # queryset = Event.objects.prefetch_related("category", "author").all()

    # # Forward ForeignKey relationship (INNER JOIN)
    queryset = Event.objects.select_related("category", "author").all()


class EventDetailView(DetailView):
    """
    http://127.0.0.1:8000/events/event/3
    Template Name ist: MODELNAME_detail.html
    generische Context-Name des Objekts ist: object
    """
    model = Event


class EventCreateView(CreateView):
    """ 
    das Default-Template einer CreateView ist _form.html
    events/event/add
    default success url = get_absolute_url() im Model definiert.
    """
    model = Event
    form_class = EventForm
    # success_url = "https://google.de"


def category_add(request: HttpRequest) -> HttpResponse:
    """
    trage eine neue Kategorie ein (stellt Form zur verfügung und 
    speichert in DB)
    events/category/add
    """
    if request.method == "POST":
        # formular Daten eintragen
        # breakpoint()
        # drei wichtige Debugger kommandos: s = stepinto, l => list, 
        # c = continue, n = next line
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            # im Erfolgsfall machen wir einen redirect auf Kategorie-Overview
            # reverse("events:categories") => {% url "events:categories" %}
            return redirect("events:categories")
    else:
        # leeres Formular zurückgeben
        form = CategoryForm()

    return render(request, "events/category_add.html", {
        "form": form,
        "title": "Neue Kategorie eintragen"
    })


def category_update(request: HttpRequest, pk: int) -> HttpResponse:
    """ 
    eine Kategorie updaten
    events/category/3/update
    """
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    
    if form.is_valid():
        form.save()
        return redirect("events:categories")

    return render(request, "events/category_add.html", {
        "form": form,
        "title": "Kategorie editieren"
    })

    


def category(request: HttpRequest, pk: int) -> HttpResponse:
    """ 
    Aufruf einer Kategorie Detailseite
    events/category/3
    """
    # try:
    #     category = Category.objects.get(pk=pk)
    # except Category.DoesNotExist:
    #     raise Http404("Diese Kategorie gibts nicht")

    category = get_object_or_404(Category, pk=pk)

    return render(request, "events/category.html", {
        "category": category
    })


def categories(request: HttpRequest) -> HttpResponse:
    """
    events/categories
    """
    categories = Category.objects.all()

    return render(request, "events/categories.html", {
        "categories": categories
    })


def hello_world(request: HttpRequest) -> HttpResponse:
    """jede View hat min. einen Parameter, das request Objekt.
    Rückgabewert jeder View ist ein HTTP-Response Objekt.
    eine Exception auslösen ist Ausnahme.

    FBV: function based views
    CBV: classed based views => modernere Ansatz
    """
    # if request.method == "POST":
    #     pass
    # else:
    #     pass
    print("Request Objekt:", request)
    print("Request Method:", request.method)
    print("Request User:", request.user)
    # print("__dict__", request.__dict__)
    qs = Category.objects.all()
    print(qs)
    return HttpResponse("hello world")
