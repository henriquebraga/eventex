from django import forms
#Se sair sem raise exception, significa que está ok.
from django.core.exceptions import ValidationError


def validate_cpf(value):
    if not value.isdigit():
        raise ValidationError('CPF deve conter apenas números', 'digits')
    if len(value) != 11:
        raise ValidationError('CPF deve conter 11 dígitos', 'length')



class SubscriptionForm(forms.Form):
    """Inherits from form base class from Django."""
    name = forms.CharField(label='Nome')
    cpf = forms.CharField(label='CPF', validators=[validate_cpf])
    email = forms.EmailField(label='E-mail')
    phone = forms.CharField(label='Telefone')