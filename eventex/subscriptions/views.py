from django.conf import settings
from django.contrib import messages
from django.core import mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm

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
        _send_mail('Confirmação de Inscrição',
                  settings.DEFAULT_FROM_EMAIL, #always import form django.conf.settings
                   form.cleaned_data['email'],
                   'subscriptions/subscription_email.txt',
                   form.cleaned_data)

        messages.success(request, 'Inscrição realizada com sucesso!')

        return HttpResponseRedirect('/inscricao/')

def new(request):
    return render(request,
                  'subscriptions/subscription_form.html',
                  context={'form': SubscriptionForm()})


def _send_mail(subject, from_, to, template_name, context):
    body = render_to_string(template_name,
                            context)
    mail.send_mail(subject,  # mail.subject
                   body,  # mail.body
                   from_,  # mail.from
                   [from_, to])  # mail.to





