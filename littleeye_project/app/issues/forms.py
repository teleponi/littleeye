from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Fieldset, Layout, Submit
from django import forms
from django.core.exceptions import ValidationError

from .models import Issue


class IssueForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Submit"))

        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-8"
        self.helper.layout = Layout(
            Fieldset(
                "Pflichtinfos",
                "name",
                "severity",
                "author",
                "media_type",
            ),
            Fieldset(
                "Beschreibung",
                "description",
                HTML(
                    """
                <div class='mb-3 row'>
                <div class='col-lg-2'></div>
                <div class='col-lg-8'>Bitte bei der Beschreibung genau
                beschreiben, wo der Fehler aufgetreten ist!
                <strong>Ansonsten kann das Ticket nicht bearbeitet werden!</strong></div>
                </div>
                """
                ),
            ),
        )

    class Meta:
        model = Issue
        fields = "__all__"
