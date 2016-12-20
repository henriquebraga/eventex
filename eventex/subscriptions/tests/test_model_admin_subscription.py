from unittest.mock import Mock

from django.test import TestCase
from django.contrib import admin
from eventex.subscriptions.admin import SubscriptionModelAdmin, Subscription, admin


class SubscriptionModelAdminTest(TestCase):

    def setUp(self):
        Subscription.objects.create(name='Henrique Braga', cpf='12345678901',
                                    email='h.braga.albor@gmail.com', phone='988591702')
        self.model_admin = SubscriptionModelAdmin(Subscription, admin.site)


    def test_is_model_admin(self):
        """SubscriptionModelAdmin Must be ModelAdmin instance type."""
        self.assertIsInstance(SubscriptionModelAdmin, type(admin.ModelAdmin))

    def test_list_display(self):
        """List display must have the following fields/order:
            name, email, phone, cpf, created_at, subscribed_today"""
        expected = ('name', 'email', 'phone', 'cpf', 'created_at', 'subscribed_today', 'paid')
        self.assertSequenceEqual(expected, SubscriptionModelAdmin.list_display)

    def test_list_filter(self):
        """List filter must have the following fields/order:
            created_at"""
        expected = ('paid', 'created_at', )
        self.assertEqual(expected, SubscriptionModelAdmin.list_filter)

    def test_search_fields(self):
        """List display must be as follows:
        name, email, phone, cpf, created_at"""
        expected = ('name', 'email', 'phone', 'cpf', 'created_at')
        self.assertSequenceEqual(expected, SubscriptionModelAdmin.search_fields)

    def test_has_action(self):
        """Action mark_as_paid should be installed."""
        model_admin = SubscriptionModelAdmin(Subscription, admin.site)
        self.assertIn('mark_as_paid', model_admin.actions)

    def test_mark_all(self):
         """Must mark all selected subscriptions as paid."""
         #Todos passados no queryset como pago
         self.call_action()
         self.assertEqual(1, Subscription.objects.filter(paid=True).count())
             #SubscriptionModelAdmin.message_user = old_message_user

    def test_message(self):
        mock = self.call_action()
        mock.assert_called_once_with(None, '1 inscrição foi marcada como paga.')

    def call_action(self):
        qs = Subscription.objects.all()
        mock = Mock()
        old_message_user = SubscriptionModelAdmin.message_user
        SubscriptionModelAdmin.message_user = mock
        # chamar a action
        self.model_admin.mark_as_paid(None, qs)
        SubscriptionModelAdmin.message_user = old_message_user
        return mock