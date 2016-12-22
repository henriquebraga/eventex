from django.conf import settings
from django.core import mail
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, resolve_url as r
from django.template.loader import render_to_string
from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def new(request):
    return create(request) \
        if request.method == 'POST' else empty_form(request)


def create(request):
        form = SubscriptionForm(request.POST)
        return success_subscription(request, form) if form.is_valid() \
            else invalid_subscription(request, form)


def empty_form(request):
    return render(request,
                  'subscriptions/subscription_form.html',
                  context={'form': SubscriptionForm()})

def success_subscription(request, form):
        subscription = form.save() #Utilize apenas quando for MUITO próximo.
        #subscription = Subscription.objects.create(**form.cleaned_data)
        _send_mail('Confirmação de Inscrição',
                  settings.DEFAULT_FROM_EMAIL, #always import form django.conf.settings
                  subscription.email,
                   'subscriptions/subscription_email.txt',
                   {'subscription': subscription})

        return HttpResponseRedirect(r('subscriptions:detail', subscription.pk).format(subscription.pk))


def invalid_subscription(request, form):
    return render(request, 'subscriptions/subscription_form.html', {'form': form})

def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name,
                            context)
    mail.send_mail(subject,
                   body,
                   from_,
                   [from_,
                    to])



def detail(request, pk):
    return render(request,
                  'subscriptions/subscription_detail.html',
                  context={'subscription': get_subscription_detail(pk)})

def get_subscription_detail(pk):
    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        raise Http404
    return subscription




