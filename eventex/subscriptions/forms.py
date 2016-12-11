from django import forms
class SubscriptionForm(forms.Form):
    """Inherits from form base class from Django."""
    name = forms.CharField(label='Nome')
    cpf = forms.CharField(label='CPF')
    email = forms.EmailField(label='E-mail')
    phone = forms.CharField(label='Telefone')