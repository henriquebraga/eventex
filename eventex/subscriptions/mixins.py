#ModelFOrmMixin: deosobre a mensagem de sucesso no model.
#BaseCreateView: ModelFormMixin, ProcessFormView. Faz a implementação de get e post
#CreateView: Une TemplateResponseMixin, BaseCreateView) - Renderizar e descobrir o nome do template
from django.core import mail
from django.template.loader import render_to_string
from django.conf import settings
from django.views.generic import CreateView


class EmailCreateMixin(object):
    email_to = None
    email_context_name = None
    email_template_name = None
    email_from = settings.DEFAULT_FROM_EMAIL
    email_subject = ''

    def send_email(self):
        subject = self.email_subject
        from_ = self.email_from  # always import form django.conf.settings
        to = self.get_email_to()
        template_name = self.get_email_template_name()
        context = self.get_email_context_data()


        body = render_to_string(template_name,
                                context)
        mail.send_mail(subject,
                       body,
                       from_,
                       [from_,
                        to])

    def get_email_to(self):
        if self.email_to:
            return self.email_to
        return self.object.email

    def get_email_context_data(self, **kwargs):
        context = dict(kwargs)
        context.setdefault(self.get_email_context_name(), self.object)
        return context

    def get_email_context_name(self):
        if self.email_context_name:
            return self.email._context_name
        return self.object._meta.model_name

    def get_email_template_name(self):
        if self.email_template_name:
            return self.email_template_name
        meta = self.object._meta
        return '{}/{}_email.txt'.format(meta.app_label, meta.model_name)

class EmailCreateView(EmailCreateMixin, CreateView):

    def form_valid(self, form):
        response = super().form_valid(form) #Faz o save
        self.send_email()
        return response
