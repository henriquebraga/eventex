from django.contrib import admin
from django.utils.timezone import now

from eventex.subscriptions.models import Subscription

class SubscriptionModelAdmin(admin.ModelAdmin):
    """Relation between django-admin and model. """
    list_display = ('name', 'email', 'phone', 'cpf', 'created_at',
                    'subscribed_today', 'paid')
    date_hierarchy = 'created_at'
    search_fields = ('name', 'email', 'phone', 'cpf', 'created_at')
    list_filter = ('paid', 'created_at', )
    actions=['mark_as_paid']


    def subscribed_today(self, obj):
        return obj.created_at == now().date

    subscribed_today.short_description = 'inscrito Hoje?'
    subscribed_today.boolean = True


    def mark_as_paid(self, request, queryset):
        count = queryset.update(paid=True)
        if count  == 1:
            msg = '{} inscrição foi marcada como paga.'
        else:
            msg = '{} inscrições foram marcadas como paga.'

        self.message_user(request, msg.format(count))

    mark_as_paid.short_description = 'Marcar como pago'

#SubscriptionModelAdmin intermedia a relação entre o modelo e o admin do Django.
admin.site.register(Subscription, SubscriptionModelAdmin)