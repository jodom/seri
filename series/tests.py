from django.core.urlresolvers import resolve
from django.shortcuts import render
from django.http import HttpRequest
from django.test import TestCase
from django.contrib.auth import authenticate, login
import re

from . import views
from . import models
from . import forms
# Create your tests here.

class SmokeTest(TestCase):

    def test_quick_math(self):
        self.assertEqual(2+2-1, 3)


class PageTests(TestCase):
    maxDiff = None

    def test_root_url_resolves_to_home_view(self):
        found = resolve('/')
        self.assertEqual(found.func, views.home)

    def strip_csrf(self, htmltext):
        """ strip the csrf value from response in order to compare templates rendered """
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', htmltext)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = views.home(request)
        expected_response = render(request, 'series/home.html')
        self.assertEqual(response.content.decode(), expected_response.content.decode())
    
    def test_new_serie_page_returns_correct_html(self):
        request = HttpRequest()
        response = views.new_serie(request)
        expected_response = render(request, 'series/new_serie.html', {'form': forms.SerieForm()})
        self.assertEqual(self.strip_csrf(response.content.decode()), \
        self.strip_csrf(expected_response.content.decode()))


    def test_see_a_new_Serie_details(self):
        request = HttpRequest()
        serie = models.Serie(title='Notes to future self')
        serie.save()
        response = views.serie_detail(request, pk=serie.pk)
        expected_response = render(
            request, 'series/serie.html',
            {'serie_title': serie.title, 'form': forms.NoteForm()})
        self.assertIn('Notes to future self', response.content.decode())
        self.assertEqual(
            self.strip_csrf(response.content.decode()),
            self.strip_csrf(expected_response.content.decode()))


class FormTests(TestCase):

    # SerieForm tests
    def test_serie_from_has_custom_fields(self):
        form = forms.SerieForm()
        self.assertIn('id="id_title_input"', form.as_p())
        self.assertIn('placeholder="Create a new Serie"', form.as_p())

class ModelTests(TestCase):

    # Serie model tests
    def test_create_and_save_new_serie(self):
        serie = models.Serie(title="Notes to future self")
        self.assertTrue(serie)
        # self.assertEqual(serie.author, 'auth.User')
        self.assertEqual(serie.title, 'Notes to future self')
        self.assertEqual(serie.limit, 100)
        self.assertTrue(serie.public)
        count_before = models.Serie.objects.count()
        serie.save()
        count_after = models.Serie.objects.count()
        self.assertLess(count_before, count_after)
