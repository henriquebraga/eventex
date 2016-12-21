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
    email = forms.EmailField(label='E-mail', required=False)
    phone = forms.CharField(label='Telefone', required=False)

    def clean_name(self):
        """Permite você implementar no formulário. Chama como complemento do campo em si.
        Chama depois do clean do CharField. SEMPRE NECESSÁRIO RETORNAR VALORES VÁLIDOS"""
        words = [w.capitalize() for w in self.cleaned_data['name'].split()]
        return ' '.join(words)

    def clean(self):
        """Chamado depois que todos os campos são validados (Ex.: Consegue validar 2 campos simultâneamente"""
        if not self.cleaned_data.get('email') and not self.cleaned_data.get('phone'):
            raise ValidationError('Informe seu e-mail ou telefone.')
        return self.cleaned_data #Precisa retornar um dicionário com os cleaned data.
