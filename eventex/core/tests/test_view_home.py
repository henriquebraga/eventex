from django.test import TestCase
from django.shortcuts import resolve_url as r
# Create your tests here.

class IndexTest(TestCase):

    def setUp(self):
        self.resp = self.client.get(r('home'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'index.html')

    def test_subscription_link(self):
        """Page must have link to /inscricao"""
        self.assertContains(self.resp, 'href="{}"'.format(r('subscriptions:new')))


