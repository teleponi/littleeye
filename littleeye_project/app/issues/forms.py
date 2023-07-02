from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Fieldset, Layout, Submit
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Issue

User = get_user_model()

labels = {
    "course": "Kurs ID",
    "media_type": "Medium",
    "tags": "Schlagworte",
    "description": "Beschreibung",
    "location": "Wo? Zeile, Minute, Seite etc.",
}


class StudentIssueForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Formular absenden"))

        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-8"
        self.helper.layout = Layout(
            Fieldset(
                "Pflichtinfos",
                "name",
                "media_type",
                "course",
                "tags",
                "location",
            ),
            Fieldset(
                "Beschreibung",
                HTML(
                    """
                <div class='mb-3 row'>
                <div class='col-lg-2'></div>
                <div class='col-lg-8'>Bitte den Fehler/das Problem genau 
                beschreiben.
                <strong>Ansonsten kann das Ticket nicht bearbeitet werden!</strong></div>
                </div>
                """
                ),
                "description",
            ),
        )

    class Meta:
        model = Issue
        fields = "__all__"
        exclude = ("author", "updated_by", "status", "severity", "is_active")

        widgets = {"tags": forms.CheckboxSelectMultiple()}
        labels = labels
