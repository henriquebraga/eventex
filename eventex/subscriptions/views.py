from django.conf import settings
from django.core import mail
from django.http import Http404
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm
from eventex.subscriptions.models import Subscription


def subscribe(request):
    return create(request) \
        if request.method == 'POST' else new(request)


def create(request):
        form = SubscriptionForm(request.POST)

        if not form.is_valid():
            return render(request, 'subscriptions/subscription_form.html', {'form': form}) #If it's not valid, return status code 200.
        else:
            return success(request, form)


def success(request, form):
        subscription = Subscription.objects.create(**form.cleaned_data)
        _send_mail('Confirmação de Inscrição',
                  settings.DEFAULT_FROM_EMAIL, #always import form django.conf.settings
                  subscription.email,
                   'subscriptions/subscription_email.txt',
                   {'subscription': subscription})

        return HttpResponseRedirect('/inscricao/{}/'.format(subscription.pk))

def new(request):
    return render(request,
                  'subscriptions/subscription_form.html',
                  context={'form': SubscriptionForm()})


def detail(request, pk):

    try:
        subscription = Subscription.objects.get(pk=pk)
    except Subscription.DoesNotExist:
        raise Http404

    return render(request, 'subscriptions/subscription_detail.html', {'subscription':
                                                                       subscription
                                                                      })


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name,
                            context)
    mail.send_mail(subject,  # mail.subject
                   body,  # mail.body
                   from_,  # mail.from
                   [from_, to])  # mail.to





