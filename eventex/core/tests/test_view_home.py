from django.test import TestCase
from django.shortcuts import resolve_url as r
# Create your tests here.
class IndexTest(TestCase):
    fixtures = ['keynotes.json']

    def setUp(self):
        self.resp = self.client.get(r('home'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'index.html')

    def test_subscription_link(self):
        """Page must have link to /inscricao"""
        self.assertContains(self.resp, 'href="{}"'.format(r('subscriptions:new')))

    def test_speakers(self):
        """Must show keynote speakers"""
        contents = [
                    'href="{}"'.format(r('speaker_detail', slug='grace-hopper')),
                    'Grace Hopper',
                    'http://hbn.link/hopper-pic',
                    'href="{}"'.format(r('speaker_detail', slug='alan-turing')),
                    'Alan Turing',
                    'http://hbn.link/turing-pic']

        for expected in contents:
            with self.subTest():
                self.assertContains(self.resp, expected)

    def test_speakers_link(self):
        expected = 'href="{}#speakers"'.format(r('home'))
        self.assertContains(self.resp, expected)


