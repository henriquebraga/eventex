from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm

class SubscribeTest(TestCase):

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
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"', 1)
        self.assertContains(self.resp, 'type="submit"', 1)

    def test_csrf(self):
        """HTML must contain CSRF. """
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form."""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """Form must have 4 fields."""
        form = self.resp.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'], list(form.fields))


class SubscribePostTest(TestCase):
    """Tests for subscription POST."""
    def setUp(self):
        data = dict(name='Henrique Braga', cpf='12345678901',
                    email='h.braga.albor@gmail.com', phone='988591702')
        self.resp = self.client.post('/inscricao/', data) #Conjunto de dados válidos.
        self.email = mail.outbox[0]


    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertEqual(302, self.resp.status_code)

    def test_send_email(self):
        """When executing POST, it should send 1 subscription e-mail"""
        self.assertEqual(1, len(mail.outbox))

    def test_email_subject(self):
        """Email subject should be 'Confirmação de Inscrição'"""
        expect = 'Confirmação de Inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_email_from(self):
        """Email from should be 'contato@eventex.com.br'"""
        expect = 'contato@eventex.com.br'
        self.assertEqual(expect, self.email.from_email)

    def test_email_to(self):
        """Email to (destiny) should be contato@eventex.com.br (where it's going to be managed)
        and 'h.braga.albor@gmail.com' (who performed the subscription itself)."""
        expect = ['contato@eventex.com.br', 'h.braga.albor@gmail.com']
        self.assertEqual(expect, self.email.to)

    def test_email_body(self):
        """Email body should contain"""
        self.assertIn('Henrique Braga', self.email.body)
        self.assertIn('12345678901', self.email.body)
        self.assertIn('h.braga.albor@gmail.com', self.email.body)
        self.assertIn('988591702', self.email.body)


class SubscribeInvalidPost(TestCase):

    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})
        self.form = self.resp.context['form']

    def test_post(self):
        """Invalid POST should not redirect. (Invalid data)"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        self.assertIsInstance(self.form, SubscriptionForm)
        #self.assertContains(form, '<form')
        #self.assertContains(form, '<input', 6)
        #self.assertContains(form, 'type="text"', 3)
        #self.assertContains(form, 'type="email"', 1)
        #self.assertContains(form, 'type="submit', 1)

    def test_form_has_error(self):
        self.assertTrue(self.form.errors)


class SubscribeSuccessMessage(TestCase):

    def test_message(self):
        data = dict(name='Henrique Braga', cpf='12345678901',
                    email='h.braga.albor@gmail.com', phone='988591702')
        resp = self.client.post('/inscricao/', data, follow=True) #follow=True Goes on with the redirect.
        self.assertContains(resp, 'Inscrição realizada com sucesso!')


