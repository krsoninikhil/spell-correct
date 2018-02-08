from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import json

class SpellCorrectTest(APITestCase):

    def __init__(self, *args):
        super().__init__(*args)
        self.url = reverse('spellcorrect')

    def test_spell_get(self):
        """Testing if get method is correcting the splleling as expected."""
        data = {'words': 'prouciation,apliction,speling'}
        res = self.client.get(self.url, data)
        self.check_response(res)

    def test_spell_post(self):
        """Testing if post method is correcting the splleling as expected."""
        data = {'words': ['prouciation', 'apliction', 'speling']}
        res = self.client.post(self.url, data, format='json')
        self.check_response(res)

    def test_spell_get_soundex(self):
        """
        Testing if get method with soundex algo is correcting the
        splleling as expected (very low accuracy).
        """
        data = {'words': 'prouciation,apliction,speling', 'method': 'soundex'}
        res = self.client.get(self.url, data)
        self.check_response_soundex(res)

    def test_spell_post_soundex(self):
        """
        Testing if post method with soundex algo is correcting the
        splleling as expected (very low accuracy).
        """
        data = {
            'words': ['prouciation', 'apliction', 'speling'],
            'method': 'soundex'
        }
        res = self.client.post(self.url, data, format='json')
        self.check_response_soundex(res)

    def check_response(self, res):
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)
        self.assertEqual(res.data['speling'], 'spelling')
        self.assertEqual(res.data['prouciation'], 'pronunciation')
        self.assertEqual(res.data['apliction'], 'application')

    def check_response_soundex(self, res):
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)
        self.assertEqual(res.data['speling'], 'supplying')
        self.assertEqual(res.data['prouciation'], 'president')
        self.assertEqual(res.data['apliction'], 'application')
