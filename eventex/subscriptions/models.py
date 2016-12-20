from django.db import models

class Subscription(models.Model):
    name = models.CharField(verbose_name='nome',max_length=100)
    cpf = models.CharField(verbose_name='CPF', max_length=11)
    email = models.EmailField(verbose_name='e-mail')
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(verbose_name='criado em',auto_now_add=True)
    paid = models.BooleanField(verbose_name='Pago', default=False)

    class Meta:
        verbose_name_plural = 'inscrições'
        verbose_name = 'inscrição'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name
