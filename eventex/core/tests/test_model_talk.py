from django.test import TestCase
from eventex.core.models import Talk


class TalkModelTest(TestCase):

    def setUp(self):
        self.talk = Talk.objects.create(
            title='Título da Palestra',
            #start='10:00',
            #description='Descrição da Palestra'
        )

    def test_create(self):
        self.assertTrue(Talk.objects.exists())

    def test_has_speakers(self):
        """Talk has many speakers and vice-versa.
            Speaker is a model manager (
            speakers: manyToManyField is a
            relatedmanager (different model field)
            Intermediary between model speaker and talk.
            Implicitily says the relation.
        """
        self.talk.speakers.create(
            name='Henrique Bastos',
            slug='henrique-bastos',
            website='http://henriquebastos.net'
        )

        self.assertEqual(1, self.talk.speakers.count())

    def test_fields_blank(self):
        self.assertFieldsCanBeBlank(Talk, ['description', 'speakers', 'start'])

    def test_start_null(self):
        field = Talk._meta.get_field('start')
        self.assertTrue(field.null)

    def test_str(self):
        expected = self.talk.title
        self.assertEqual(expected, str(self.talk))

    def assertFieldsCanBeBlank(self, klass, field_names):
        for field in field_names:
            with self.subTest():
                field = klass._meta.get_field(field)
                self.assertTrue(field.blank)

