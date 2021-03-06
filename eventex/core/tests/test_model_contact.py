from django.core.exceptions import ValidationError
from django.test import TestCase
from eventex.core.models import Speaker, Contact

class ContactModelTest(TestCase):


        def setUp(self):
            self.speaker = Speaker.objects.create(name='Henrique Braga',
                                         slug='henrique-braga',
                                         photo='http://hbn.link/hb-pic')


        def test_email(self):
            contact = Contact.objects.create(speaker=self.speaker,
                                         knd=Contact.EMAIL,
                                         value='h.braga.albor@gmail.com')
            self.assertTrue(Contact.objects.exists())

        def test_phone(self):
            contact = Contact.objects.create(speaker=self.speaker,
                                             knd=Contact.PHONE,
                                             value='11-98859-1702')
            self.assertTrue(Contact.objects.exists())

        def test_choices(self):
            """Contact kind must be limited to E or P"""
            contact = Contact.objects.create(speaker=self.speaker,
                                             knd='Z',
                                             value='B')
            self.assertRaises(ValidationError, contact.full_clean)

        def test_str(self):
            contact = Contact(speaker=self.speaker,
                            knd='E',
                            value='h.braga.albor@gmail.com')
            self.assertEqual('h.braga.albor@gmail.com', str(contact))

class ContactManagerTest(TestCase):

    def setUp(self):
        s = Speaker.objects.create(
            name='Henrique Braga',
            slug='henrique-braga',
            photo='http://hbn.link/hb-pic'
        )
        s.contact_set.create(knd=Contact.EMAIL, value='h.braga.albor@gmail.com')
        s.contact_set.create(knd=Contact.PHONE, value='988591702')

    def test_emails(self):
        qs = Contact.objects.emails()
        expected = ['h.braga.albor@gmail.com']
        self.assertQuerysetEqual(qs, expected, transform=lambda o : o.value)

    def test_phones(self):
        qs = Contact.objects.phones()
        expected = ['988591702']
        self.assertQuerysetEqual(qs, expected, transform=lambda o : o.value)