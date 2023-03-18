from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Button,
    Field,
    Layout,
    Row,
    Submit,
    Reset
)
    
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_id = "form-container"

        self.helper.layout = Layout(
            Row(
                Field("name", css_class="form-control"),
                Field("item_type", css_class="form-control"),
                Field("ordertype", css_class="form-control"),
                Field("price", css_class="form-control"),
            )
        )
        self.helper.add_input(Submit("save", "save", css_class="btn-primary"))
        self.helper.add_input(Button("button", "Add", css_class="btn-dark"))
        self.helper.add_input(Reset("reset", "Reset", css_class="btn-success"))
        self.helper.template = "bootstrap/table_inline_formset.html"


class CleanOrderFormset(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = True

    def __add_fields(self, form, index):
        super().add_fields(form, index)
        form.fields["dello"] = forms.CharField(required=False)

    def clean(self) -> None:
        """example validation process.
        we do not return any data here (which is usually the case)
        """

        if any(self.errors):
            pass

        for form in self.forms:
            if cleaned_data := form.cleaned_data:

                if "price" in cleaned_data and cleaned_data["price"] < 0:
                    form._errors["price"] = self.error_class(
                        ["Der Preis ist fehlerhaft."])

                if "name" in cleaned_data and len(cleaned_data["name"]) < 3:
                    form._errors["name"] = self.error_class(
                        ["Der Name ist zu kurz."])


OrderFormSet = forms.modelformset_factory(
    Order,
    extra=1,
    formset=CleanOrderFormset,
    fields=["item_type", "name", "ordertype", "price"],
)
