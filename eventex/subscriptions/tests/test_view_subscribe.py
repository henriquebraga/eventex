from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscribeGet(TestCase):

    def setUp(self):
        self.resp = self.client.get('/inscricao/')

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




class SubscribePostValid(TestCase):
    """Tests for subscription POST."""
    def setUp(self):
        data = dict(name='Henrique Braga', cpf='12345678901',
                    email='h.braga.albor@gmail.com', phone='988591702')
        self.resp = self.client.post('/inscricao/', data) #Conjunto de dados válidos.
        self.email = mail.outbox[0] #There's only one e-mail.


    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertEqual(302, self.resp.status_code)

    def test_send_email(self):
        """View must should sent 1 email."""
        self.assertEqual(1, len(mail.outbox))


class SubscribePostInvalid(TestCase):

    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})
        self.form = self.resp.context['form']

    def test_post(self):
        """Invalid POST should not redirect. (Invalid data)"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        """Form must be a SubscriptionForm type"""
        self.assertIsInstance(self.form, SubscriptionForm)

    def test_form_has_error(self):
        self.assertTrue(self.form.errors)


class SubscribeSuccessMessage(TestCase):

    def test_message(self):
        data = dict(name='Henrique Braga', cpf='12345678901',
                    email='h.braga.albor@gmail.com', phone='988591702')
        resp = self.client.post('/inscricao/', data, follow=True) #follow=True Goes on with the redirect.
        self.assertContains(resp, 'Inscrição realizada com sucesso!')


