from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button
from .models import Category, Event


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.add_input(Submit('submit', "Abschicken"))
    
    class Meta:
        model = Event
        fields = "__all__"

        widgets = {
            "date": forms.DateInput(
                format=("%Y-%m-%d %H:%M"), attrs={"type": "datetime-local"}
            ),
            "min_group": forms.RadioSelect()
        }

        labels = {
            "name": "Was geht ab?",
            "min_group": "Mindestgruppe",
        }
    
    def clean_sub_title(self) -> str:
        """Das Feld sub_title bereinigen und im Falle
        des Falles einen ValidationError auslösen.
        
        Schema der clean-Methoden: def clean_FELDNAME(self)
        Rückgabe  muss der Feldwert sein.
        """
        sub_title = self.cleaned_data["sub_title"]
        
        if isinstance(sub_title, str):

            # von Hashmarks bereinigen
            sub_title = sub_title.replace("#", "")

            # Validation Error auslösen, falls ein @ Symbol im Sub_title
            if "@" in sub_title:
                raise ValidationError("Das @-Symbol ist im Subtitle nicht legal.")

        return sub_title
    
    def clean(self) -> dict:
        """für feldübergreifende Validierung"""
        super().clean()  # erzeugt self.cleaned_data

        name = self.cleaned_data.get("name")
        sub_title = self.cleaned_data.get("sub_title")
        if isinstance(sub_title, str) and isinstance(name, str):

            if name in sub_title:
                
                self._errors["sub_title"] = self.error_class(
                    ["Bitte mal den Subtitle prüfen!"]
                )
                
                self._errors["name"] = self.error_class(
                    ["Name ist im Subtitle."]
                )

                raise ValidationError("Der Name darf nicht im Subtitle sein")
                
        return self.cleaned_data


class CategoryForm(forms.ModelForm):
    """ 
    forms.ModelForm => Formular basiert auf unserem
    Category - Model
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        # self.helper.form_class = "form-horizontal"
        # self.helper.label_class = 'col-lg-2'
        # self.helper.field_class = 'col-lg-8'
        self.helper.add_input(Submit('submit', "Abschicken"))


    class Meta:
        model = Category
        fields = "__all__"  # alle Felder nutzen
        # exclude = "name", # Name Feld excludieren

    # zustäliches Feld
    message = forms.CharField(max_length=10, required=False)
