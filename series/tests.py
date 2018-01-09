from django.core.urlresolvers import resolve
from django.shortcuts import render
from django.http import HttpRequest
from django.test import TestCase
import re

from .views import home
# Create your tests here.

class SmokeTest(TestCase):

    def test_quick_math(self):
        self.assertEqual(2+2-1, 3)


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def strip_csrf(self, htmltext):
        """ strip the csrf value from response in order to compare templates rendered """
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', htmltext)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home(request)
        expected_response = render(request, 'seris/home.html')
        self.assertEqual(self.strip_csrf(response.content.decode()), \
        self.strip_csrf(expected_response.content.decode()))

    def test_home_page_can_save_a_POST_request(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['serie'] = 'Notes to future self'

        response = home(request)

        self.assertIn('Notes to future self', response.content.decode())
