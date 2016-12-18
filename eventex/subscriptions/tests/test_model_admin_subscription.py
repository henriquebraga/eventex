from django.test import TestCase
from django.contrib import admin
from eventex.subscriptions.admin import SubscriptionModelAdmin


class SubscriptionModelAdminTest(TestCase):

    def test_is_model_admin(self):
        """SubscriptionModelAdmin Must be ModelAdmin instance type."""
        self.assertIsInstance(SubscriptionModelAdmin, type(admin.ModelAdmin))

    def test_list_display(self):
        """List display must have the following fields/order:
            name, email, phone, cpf, created_at, subscribed_today"""
        expected = ('name', 'email', 'phone', 'cpf', 'created_at', 'subscribed_today')
        self.assertSequenceEqual(expected, SubscriptionModelAdmin.list_display)

    def test_list_filter(self):
        """List filter must have the following fields/order:
            created_at"""
        expected = ('created_at',)
        self.assertEqual(expected, SubscriptionModelAdmin.list_filter)

    def test_search_fields(self):
        """List display must be as follows:
        name, email, phone, cpf, created_at"""
        expected = ('name', 'email', 'phone', 'cpf', 'created_at')
        self.assertSequenceEqual(expected, SubscriptionModelAdmin.search_fields)