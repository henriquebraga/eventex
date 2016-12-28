from datetime import datetime
from django.test import TestCase
from eventex.subscriptions.models import Subscription
from django.shortcuts import resolve_url as r


class SubscriptionModelTest(TestCase):

    def setUp(self):
        self.obj = Subscription(name='Henrique Braga',
                                cpf='12345678901',
                                email='h.braga.albor@gmail.com',
                                phone='988591702')
        self.obj.save()

    def test_create(self):
        """Must create a subscription."""
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        """Subscription must have an auto created_at attr."""
        self.assertIsInstance(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Henrique Braga', str(self.obj))

    def test_paid_default_false(self):
        """By default, paid must be false."""
        self.assertEqual(False, self.obj.paid)

    def test_get_absolute_url(self):
        url = r('subscriptions:detail', self.obj.pk)
        self.assertEqual(url, self.obj.get_absolute_url())




