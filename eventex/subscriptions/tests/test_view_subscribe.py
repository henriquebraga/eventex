from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


class SubscriptionsNewGet(TestCase):

    def setUp(self):
        self.resp = self.client.get(r('subscriptions:new'))

    def test_get(self):
        """GET /inscricao/ must return status code 200."""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """HTML must contains input tags. (1 form, 5 inputs (3 text, 1 email and 1 submit button)"""
        TAGS = (
            ('<form', 1),
            ('<input', 6),
            ('type="text"', 3),
            ('type="email', 1),
            ('type="submit"', 1)
        )

        for tag, count in TAGS:
            # Accumulates exceptions. One test- many assertions.
            with self.subTest():
                self.assertContains(self.resp, tag, count)

    def test_csrf(self):
        """HTML must contain CSRF. """
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form."""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)




class SubscriptionsNewPost(TestCase):
    """Tests for subscription POST."""

    def setUp(self):
        data = dict(name='Henrique Braga', cpf='12345678901',
                    email='h.braga.albor@gmail.com', phone='988591702')
        self.resp = self.client.post(r('subscriptions:new'), data) #Conjunto de dados válidos.
        self.email = mail.outbox[0] #There's only one e-mail.


    def test_post(self):
        """Valid POST should redirect to /inscricao/1/"""
        self.assertRedirects(self.resp,r('subscriptions:detail', 1))

    def test_send_email(self):
        """View must should sent 1 email."""
        self.assertEqual(1, len(mail.outbox))

    def test_save(self):
        """Subscription must be saved."""
        self.assertTrue(Subscription.objects.exists())


class SubscribePostInvalid(TestCase):

    def setUp(self):
        self.resp = self.client.post(r('subscriptions:new'), {})
        self.form = self.resp.context['form']

    def test_post(self):
        """Invalid POST should not redirect. (Invalid data)"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Must use template subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        """Form must be a SubscriptionForm type"""
        self.assertIsInstance(self.form, SubscriptionForm)

    def test_form_has_error(self):
        """Form must have errors."""
        self.assertTrue(self.form.errors)

    def test_do_not_save(self):
        """Subscription must not be saved."""
        self.assertFalse(Subscription.objects.exists())

class TemplateRegressionTest(TestCase):

    def test_template_has_non_field_errors(self):
        invalid_data = dict(name='Henrique Braga', cpf='12345678901')
        response = self.client.post(r('subscriptions:new'), invalid_data)
        self.assertContains(response, '<ul class="errorlist nonfield">')



