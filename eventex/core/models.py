from django.db import models
from django.shortcuts import resolve_url as r

from eventex.core.managers import KindQuerySet, StartManager, StartQuerySet


class Speaker(models.Model):
    name = models.CharField('nome', max_length=255)
    slug = models.SlugField('slug')
    photo = models.URLField('foto')
    website = models.URLField('website', blank=True)
    description = models.TextField('descrição', blank=True)

    class Meta:
        verbose_name = 'Palestrante'
        verbose_name_plural = 'Palestrantes'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return r('speaker_detail', slug=self.slug)


class Contact(models.Model):
    EMAIL = 'E'
    PHONE = 'P'
    speaker = models.ForeignKey('Speaker', verbose_name='palestrante') #Sabe previamente os modelos disponíveis.
    KINDS = (
               ('E', 'Email'),
               ('P', 'Telefone'),
             )

    knd = models.CharField('tipo',max_length=1, choices=KINDS)
    value = models.CharField('contato',max_length=255)

    objects = KindQuerySet.as_manager()

    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'

    def __str__(self):
        return self.value

class Talk(models.Model):
    title = models.CharField('título',max_length=200)
    start = models.TimeField('início', blank=True, null=True)
    description = models.TextField('descrição', blank=True)
    speakers = models.ManyToManyField('Speaker', verbose_name='palestrantes', blank=True)
    objects = StartQuerySet.as_manager()
    class Meta:
        verbose_name_plural = 'palestras'
        verbose_name = 'palestra'

    def __str__(self):
        return self.title



