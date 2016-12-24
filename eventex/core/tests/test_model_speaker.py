from django.test import TestCase
from eventex.core.models import Speaker
from django.shortcuts import resolve_url as r


class SpeakerModelTest(TestCase):


    def setUp(self):
        self.speaker = Speaker.objects.create(
            name='Grace Hopper',
            slug='grace-hopper',
            photo='http://hbn.link/hopper-pic',
            website='http://hbn.link/hopper-site',
            description='Programadora e Almirante'
        )

    def test_create(self):
        self.assertTrue(Speaker.objects.exists())


    def test_fields_can_be_blank(self):
        self.assertFieldsCanBeBlank(Speaker, ['website', 'description'])

    def test_str(self):
        self.assertEqual('Grace Hopper', str(self.speaker))

    def test_get_absolute_url(self):
        url = r('speaker_detail', slug=self.speaker.slug)
        self.assertEqual(url, self.speaker.get_absolute_url())

    def assertFieldsCanBeBlank(self, klass, field_names):
        for field in field_names:
            with self.subTest():
                field = klass._meta.get_field(field)
                self.assertTrue(field.blank)


