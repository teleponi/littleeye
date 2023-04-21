from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError

User = get_user_model()


class ContactForm(forms.Form):
    pass


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, label="Erinnere dich")


def validate_email(value):
    """Validate an email if unique."""
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            f"{value} ist schon in Benutzung.",
            params={'value': value})


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )
        labels = {"privacy": "Datenschutzerklärung"}

    email = forms.EmailField(validators=[validate_email])  # check uniqe email
    privacy = forms.BooleanField(required=False)

    def clean_privacy(self) -> str:
        """Die Datenschutzerklärung muss angeglickt werden. Falls die Checkbox
        nicht angelegt wurde, wird ein ValidationError ausgelöst"""

        privacy = self.cleaned_data["privacy"]
        if not privacy:
            raise ValidationError(
                """Bitte bestätigen Sie, dass Sie die
                Datenschutzerklärung gelesen haben"""
            )
        return privacy
