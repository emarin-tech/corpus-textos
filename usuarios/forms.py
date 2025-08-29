from django import forms
from django.core.exceptions import ValidationError
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

Usuario = get_user_model()

class RegistroForm(forms.Form):
    email = forms.EmailField(
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "tu@correo.com"})
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Repite la contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    acepta_condiciones = forms.BooleanField(
        label="Acepto las condiciones y la política de privacidad.",
        required=True,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input", "id": "id_acepta_condiciones"})
    )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if Usuario.objects.filter(correo_electronico__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con este correo.")
        return email

    def clean(self):
        data = super().clean()
        p1, p2 = data.get("password1"), data.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden.")
        if p1:
            validate_password(p1)
        return data

class UsuarioPerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["nombre","apellidos","titulo","telefono","foto",
                  "calle","ciudad","provincia","codigo_postal","pais"]
        widgets = {
            "titulo": forms.TextInput(attrs={"placeholder": "p. ej., Dr., Ing., Lic."}),
            "telefono": forms.TextInput(attrs={"placeholder": "+34 600 123 123"}),
            "calle": forms.TextInput(attrs={"placeholder": "Calle y nº"}),
            "ciudad": forms.TextInput(attrs={"placeholder": "Ciudad"}),
            "provincia": forms.TextInput(attrs={"placeholder": "Provincia/Estado"}),
            "codigo_postal": forms.TextInput(attrs={"placeholder": "Código Postal"}),
            "pais": forms.TextInput(attrs={"placeholder": "País"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "foto":
                field.widget.attrs.setdefault("class", "form-control")  # file input
            else:
                field.widget.attrs.setdefault("class", "form-control")


class UsuarioPrivacidadForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            "acepta_politica_datos","acepta_correo_electronico","acepta_correo_postal",
            "acepta_boletin","acepta_publicacion_contenido","acepta_condiciones_servicio",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-check-input")


class UsuarioCorreoForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["correo_electronico"]

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop("usuario", None)
        super().__init__(*args, **kwargs)
        self.fields["correo_electronico"].widget.attrs.setdefault("class", "form-control")
        if self.usuario and self.usuario.google_id:
            self.fields["correo_electronico"].disabled = True
            self.fields["correo_electronico"].help_text = "Correo gestionado por Google; cambio deshabilitado."
        else:
            self.fields["correo_electronico"].help_text = "Se utiliza para iniciar sesión."
