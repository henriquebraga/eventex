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
        self.assertContains(self.resp, 'href="/inscricao/')


class InvalidPage(TestCase):
    """Tests for invalid URL."""

    def setUp(self):
        self.resp = self.client.get('/not-exists')

    def test_get(self):
        """Status code must return 404 (Not Found)."""
        self.assertEqual(404, self.resp.status_code)

    def test_template(self):
        """Must use template 404.html (Django convention for Not Found)."""
        self.assertTemplateUsed(self.resp, '404.html')