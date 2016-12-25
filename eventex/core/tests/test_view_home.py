from django.test import TestCase
from django.shortcuts import resolve_url as r


def to_href(to, slug=None):
    """A useful shortcut to format a link properly to href tag"""
    href_tag = 'href="{}"'
    return href_tag.format(r(to, slug=slug)) if slug else href_tag.format(r(to))

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
        self.assertContains(self.resp, to_href('subscriptions:new'))
                            #'href="{}"'.format(r('subscriptions:new')))

    def test_speakers(self):
        """Must show keynote speakers"""
        contents = [
                    to_href('speaker_detail', slug='grace-hopper'),
                    'Grace Hopper',
                    'http://hbn.link/hopper-pic',
                    to_href('speaker_detail', slug='alan-turing'),
                    'Alan Turing',
                    'http://hbn.link/turing-pic']

        for expected in contents:
            with self.subTest():
                self.assertContains(self.resp, expected)

    def test_speakers_link(self):
        expected = 'href="{}#speakers"'.format(r('home'))
        self.assertContains(self.resp, expected)

    def test_talks_link(self):
        expected = to_href('talk_list')
        self.assertContains(self.resp, expected)


class TalkListGetEmpty(TestCase):

    def test_get_empty(self):
        response = self.client.get(r('talk_list'))
        message = 'Ainda não existem palestras de {}.'
        messages = [message.format('manhã'),
                    message.format('tarde')]

        for expected in messages:
            with self.subTest():
                self.assertContains(response, expected)
