from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import DeleteView, UpdateView

from .forms import OrderForm, OrderFormSet
from .models import Order


class OrderDeleteView(DeleteView):
    """
    orders/order/delete/3
    """
    model = Order
    success_url = reverse_lazy("orders:order_create")


class OrderUpdateView(UpdateView):
    """
    orders/order/update/3
    """
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy("orders:order_create")


class OrderCreateView(TemplateView):
    """
    /orders/order/create
    """
    template_name = "orders/multiform.html"
    form = OrderForm()

    def get(self, *args, **kwargs) -> HttpResponse:
        formset = OrderFormSet(queryset=Order.objects.none())
        orders = Order.objects.all()

        return self.render_to_response(
            {
                "formset": formset,
                "orders": orders,
                "helper": self.form.helper,
            }
        )

    def post(self, *args, **kwargs) -> HttpResponse:
        formset = OrderFormSet(data=self.request.POST)
        if formset.is_valid():
            formset.save()
            return redirect(reverse_lazy("orders:order_create"))

        return self.render_to_response(
            {
                "formset": formset,
                "orders": Order.objects.all(),
                "helper": self.form.helper,
            }
        )
