# corpus/forms.py
from django import forms

class SuscripcionForm(forms.Form):
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Tu correo electrónico",
            "required": "required"
        })
    )
