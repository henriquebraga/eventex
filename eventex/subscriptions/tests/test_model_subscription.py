from datetime import datetime
from django.test import TestCase
from eventex.subscriptions.models import Subscription

class SubscriptionModelTest(TestCase):

    def setUp(self):
        self.obj = Subscription(name='Henrique Braga',
                                cpf='12345678901',
                                email='h.braga.albor@gmail.com')
        self.obj.save()
    def test_create(self):
        """Must create a subscription."""

        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        """Subscription must have an auto created_at attr."""
        self.assertIsInstance(self.obj.created_at, datetime)
