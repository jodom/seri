from django.core.urlresolvers import resolve
from django.test import TestCase
from .views import home
# Create your tests here.

class SmokeTest(TestCase):

    def test_quick_math(self):
        self.assertEqual(2+2-1, 3)


class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home)