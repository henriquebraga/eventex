from django.test import TestCase


class NotFoundPage(TestCase):
    """Tests for invalid URL."""

    def setUp(self):
        self.resp = self.client.get('/not-exists')

    def test_get(self):
        """Status code must return 404 (Not Found)."""
        self.assertEqual(404, self.resp.status_code)

    def test_template(self):
        """Must use template 404.html (Django convention for Not Found)."""
        self.assertTemplateUsed(self.resp, '404.html')