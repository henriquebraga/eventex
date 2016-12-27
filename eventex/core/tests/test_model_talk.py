from django.test import TestCase

from eventex.core.managers import StartManager
from eventex.core.models import Talk, Speaker, CourseOld, Course


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


class TalkManagerTest(TestCase):

    def setUp(self):
        talk_morning = Talk.objects.create(
            title='Palestra com início até 12:00',
            start='10:00',
            description='Descrição da Palestra'
        )

        talk_afternoon = Talk.objects.create(
            title='Palestras com início depois do 12:00',
            start='13:00',
            description='Descrição da Palestra'
        )

        s1 = Speaker.objects.create(
            name='Grace Hopper',
            slug='grace-hopper',
            photo='http://hbn.link/hopper-pic',
            website='http://hbn.link/hopper-site',
            description='Programadora e Almirante'
        )
        talk_morning.speakers.add(s1)

    def test_morning(self):
        qs = Talk.objects.morning()
        expected = ['Palestra com início até 12:00']
        self.assertQuerysetEqual(qs, expected, transform=lambda o : o.title)

    def test_afternoon(self):
        qs = Talk.objects.afternoon()
        expected = ['Palestras com início depois do 12:00']
        self.assertQuerysetEqual(qs, expected, transform=lambda o : o.title)



class CourseOldModelTest(TestCase):

    def setUp(self):
        self.course = CourseOld.objects.create(
            title='Título do Curso',
            start='09:00',
            description='Descrição do curso.',
            slots=20
        )

    def test_create(self):
        self.assertTrue(CourseOld.objects.exists())

    def test_has_many_speakers(self):
        """Test relation between speakers"""
        self.course.speakers.create(
            name='Henrique Braga',
            slug='henrique-braga',
            website='http://henriquebraga.net'
        )
        self.assertEqual(1, self.course.speakers.count())

    def test_str(self):
        self.assertEqual('Título do Curso', str(self.course))

    def test_manager(self):
        self.assertIsInstance(CourseOld.objects, StartManager)

class CourseModelTest(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            title='Título do Curso',
            start='09:00',
            description='Descrição do curso.',
            slots=20
        )

    def test_create(self):
        self.assertTrue(Course.objects.exists())

    def test_has_many_speakers(self):
        """Test relation between speakers"""
        self.course.speakers.create(
            name='Henrique Braga',
            slug='henrique-braga',
            website='http://henriquebraga.net'
        )
        self.assertEqual(1, self.course.speakers.count())

    def test_str(self):
        self.assertEqual('Título do Curso', str(self.course))

    def test_manager(self):
        self.assertIsInstance(Course.objects, StartManager)