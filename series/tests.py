from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from .views import home
# Create your tests here.

class SmokeTest(TestCase):

    def test_quick_math(self):
        self.assertEqual(2+2-1, 3)


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>Seris, a note a day</title>',
                      response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
