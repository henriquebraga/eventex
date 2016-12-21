from django.test import TestCase

from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):
    """Tests for SubscriptionForm"""


    def test_form_has_fields(self):
        """Form must have 4 fields."""
        form = SubscriptionForm()
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))

    def test_cpf_is_digit(self):
        """CPF must only accept digits."""
        form = self.make_validated_form(cpf='ABCD5678901')
        self.assertFormErrorCode(form , 'cpf', 'digits')


    def test_cpf_has_11_digits(self):
        """CPF must have 11 digits."""
        form = self.make_validated_form(cpf='1234')

        self.assertFormErrorCode(form, 'cpf', 'length')

    def test_must_be_capitalized(self):
        form = self.make_validated_form(name='HENRIQUE BRAGA')
        self.assertEqual('Henrique Braga', form.cleaned_data['name'])

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)

    def assertFormErrorMessage(self, form, field, message):
        errors = form.errors
        errors_list = errors[field]
        self.assertListEqual([message], errors_list)

    def make_validated_form(self, **kwargs):
        """Create by default a validated form (it depends on what kwargs contains)"""
        valid = dict(name='Henrique Braga',
                                cpf='41941833802',
                                email='h.braga.albor@gmail.com',
                                phone='988591702')
        data = dict(valid, **kwargs)
        form = SubscriptionForm(data)
        form.is_valid()
        return form

