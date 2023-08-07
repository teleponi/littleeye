from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Fieldset, Layout, Submit, Button
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import Ticket, Comment, Status

User = get_user_model()

labels = {
    "course": "Kurs ID",
    "media_type": "Medium",
    "tags": "Schlagworte",
    "description": "Beschreibung",
    "location": "Wo? Zeile, Minute, Seite etc.",
    "name": "Titel",
    "severity": "Schweregrad",
}


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "name",
            "description",
            HTML(
                """
                <div>
                <button class='btn btn-green float-end'
                style='margin-left:10px'>Kommentar hinzufügen</button>
                <button id="returnbutton" type="button" class='btn btn-secondary float-end '>Zurück zur
                Detailseite</button>
                </div>
                <div class="clearfix"></div>
                """
            ),
        )

    class Meta:
        model = Comment
        fields = "__all__"
        exclude = ("author", "ticket")
        labels = {"name": "Titel", "description": "Beschreibung"}


class StudentTicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-9"
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
            HTML(
                """
                <div class='mb-3 row'>
                <div class='col-lg-2'></div>
                <div class='col-lg-9'>
                <button class='btn btn-green float-end' style='margin-left:10px'>Ticket absenden</button>
                <a href="/">
                <button type="button" class='btn btn-secondary float-end '>Zurück zur
                Übersicht</button></a>
                </div>
                """
            ),
        )

    class Meta:
        model = Ticket
        fields = "__all__"
        exclude = ("author", "updated_by", "status", "severity")

        widgets = {"tags": forms.CheckboxSelectMultiple()}
        labels = labels


class TutorTicketForm(StudentTicketForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        limited_choices = [s for s in Status.choices if s[0] not in [0, 3]]
        self.fields["status"] = forms.ChoiceField(choices=limited_choices)

        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-8"
        self.helper.layout = Layout(
            "severity",
            "status",
            HTML(
                """
                <div class='custom-padding-ticket'>
                <button class='btn btn-green float-end'
                style='margin-left:10px'>Speichern</button>
                <button id='returnbutton' type="button" class='btn btn-secondary float-end '>Zurück zur
                Detailseite</button>
                </div>
                <div class="clearfix"></div>
                """
            ),
        )

    class Meta(StudentTicketForm.Meta):
        exclude = (
            "author",
            "updated_by",
            "name",
            "media_type",
            "course",
            "tags",
            "location",
            "description",
        )
