from django.db import models



class KindQuerySet(models.QuerySet):

    def emails(self):
        return self.filter(knd=self.model.EMAIL)

    def phones(self):
        return self.filter(knd=self.model.PHONE)


class KindContactManager(models.Manager):

    def get_queryset(self):
        return KindQuerySet(self.model, using=self.db)

    def emails(self):
        return self.get_queryset().emails()

    def phones(self):
        return self.get_queryset().phones()


class StartQuerySet(models.QuerySet):
    MIDDAY= '12:00'

    def morning(self):
        return self.filter(start__lt=self.MIDDAY)

    def afternoon(self):
        return self.filter(start__gte=self.MIDDAY)


class StartManager(models.Manager):

    def get_queryset(self):
        return StartQuerySet(self.model, using=self.db)

    def morning(self):
        return self.get_queryset().morning()

    def afternoon(self):
        return self.get_queryset().afternoon()

