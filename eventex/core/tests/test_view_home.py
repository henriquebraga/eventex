from django.test import TestCase

# Create your tests here.

class IndexTest(TestCase):

    def setUp(self):
        self.resp = self.client.get('/')

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'index.html')

    def test_subscription_link(self):
        """Page must have link to /inscri"""
        self.assertContains(self.resp, 'href="/inscricao/')


