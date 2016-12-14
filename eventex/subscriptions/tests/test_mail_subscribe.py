from django.core import mail
from django.test import TestCase
class MailSubscribe(TestCase):
    def setUp(self):
        data = dict(name='Henrique Braga', cpf='12345678901',
                    email='h.braga.albor@gmail.com', phone='988591702')
        self.resp = self.client.post('/inscricao/', data) #Conjunto de dados válidos.
        self.email = mail.outbox[0] #There's only one e-mail.



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
        contents = ( 'Henrique Braga',
                    '12345678901',
                    'h.braga.albor@gmail.com' ,
                    '988591702' )

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)

