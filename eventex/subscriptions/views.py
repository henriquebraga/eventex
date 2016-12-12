from django.contrib import messages
from django.core import mail
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string

from eventex.subscriptions.forms import SubscriptionForm

def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        #fullclean - Passa pelos filtros (dados sanitizados)
        if form.is_valid():
            #Hard coded to pass the test! Must use POST content from request.
            #context = dict(name='Henrique Braga', cpf='12345678901',
            #               email='h.braga.albor@gmail.com', phone='988591702')

            #If no errors, sends an email and redirect.
            body = render_to_string('subscriptions/subscription_email.txt',
                                   form.cleaned_data)
            #Must send email...
            mail.send_mail('Confirmação de Inscrição', #mail.subject
                           body, #mail.body
                           'contato@eventex.com.br', #mail.from
                           ['contato@eventex.com.br', form.cleaned_data['email']]) #mail.to

            messages.success(request, 'Inscrição realizada com sucesso!')
            #And redirect to /inscricao/
            return HttpResponseRedirect('/inscricao/')
        else:
            return render(request, 'subscriptions/subscription_form.html', {'form': form}) #If it's not valid, return status code 200.
    else:
        context = {'form': SubscriptionForm()} #Associa uma instância de SubscriptionForm.
        return render(request, 'subscriptions/subscription_form.html', context)




