from django.core.urlresolvers import resolve
from django.shortcuts import render
from django.http import HttpRequest
from django.test import TestCase
from django.contrib.auth import authenticate, login
import re

from .views import home, new_serie, serie_detail, add_note
from .models import Serie, Note
from .forms import SerieForm, NoteForm
# Create your tests here.

class SmokeTest(TestCase):

    def test_quick_math(self):
        self.assertEqual(2+2-1, 3)


class PageTests(TestCase):
    maxDiff = None

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
        expected_response = render(request, 'series/home.html', {'form': NoteForm()})
        self.assertEqual(
            self.strip_csrf(response.content.decode()),
            self.strip_csrf(expected_response.content.decode()))
    
    def test_home_page_redirects_after_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['content'] = 'Sample Note'
        response = home(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/serie/1/')


class SerieTest(TestCase):
    def test_new_serie_detail_uses_correct_template(self):
        response = self.client.get('/serie/new/')
        self.assertTemplateUsed(response, 'series/new_serie.html')

    def test_serie_detail_uses_serie_template(self):
        serie = Serie.objects.create(title='My Serie')
        response = self.client.get('/serie/{id}/'.format(id=serie.id))
        self.assertTemplateUsed(response, 'series/serie.html')

    def test_see_serie_details_with_all_notes_displayed(self):
        serie = Serie.objects.create(title='My Serie')
        Note.objects.create(content="Note number uno", serie=serie)
        Note.objects.create(content="Note number dos", serie=serie)
        response = self.client.get('/serie/1/')
        self.assertContains(response, 'My Serie')
        self.assertContains(response, 'Note number uno')
        self.assertContains(response, 'Note number dos')

    def test_each_serie_displays_only_its_notes(self):
        serie1 = Serie.objects.create(title="First Serie")
        Note.objects.create(content="Note number uno serie Uno", serie=serie1)
        Note.objects.create(content="Note number dos serie Uno", serie=serie1)

        serie2 = Serie.objects.create(title="Second Serie")
        Note.objects.create(content="Note number uno serie Dos", serie=serie2)
        Note.objects.create(content="Note number dos serie Dos", serie=serie2)

        response1 = self.client.get('/serie/{id}/'.format(id=serie1.id))
        self.assertContains(response1, "Note number uno serie Uno")
        self.assertContains(response1, "Note number dos serie Uno")
        self.assertNotContains(response1, "Note number uno serie Dos")
        self.assertNotContains(response1, "Note number dos serie Dos")

        response1 = self.client.get('/serie/{id}/'.format(id=serie2.id))
        self.assertContains(response1, "Note number dos serie Dos")
        self.assertContains(response1, "Note number uno serie Dos")
        self.assertNotContains(response1, "Note number uno serie Uno")
        self.assertNotContains(response1, "Note number dos serie Uno")

    def test_save_note_to_existing_list_via_POST(self):
        serie = Serie.objects.create(title='My Serie')
        Note.objects.create(content="First note to My Serie", serie=serie)
        self.assertEqual(Note.objects.count(), 1)
        self.client.post(
            '/serie/{id}/add_note'.format(id=serie.id),
            data={'content': 'An additional note to My Serie'}
        )
        self.assertEqual(Note.objects.count(), 2)
        second_note = Note.objects.last()
        self.assertEqual(second_note.serie, serie)


class FormTests(TestCase):

    # SerieForm tests
    def test_serie_form_has_custom_fields(self):
        form = SerieForm()
        self.assertIn('id="id_title_input"', form.as_p())
        self.assertIn('placeholder="Enter Title"', form.as_p())

    def test_note_form_has_custom_fields(self):
        form = NoteForm()
        self.assertIn('id="id_new_note"', form.as_p())
        self.assertIn('placeholder="Add note"', form.as_p())


class ModelTests(TestCase):

    # Serie model tests
    def test_create_and_save_new_serie(self):
        serie = Serie(title="Notes to future self")
        self.assertTrue(serie)
        # self.assertEqual(serie.author, 'auth.User')
        self.assertEqual(serie.title, 'Notes to future self')
        self.assertEqual(serie.limit, 100)
        self.assertTrue(serie.public)
        count_before = Serie.objects.count()
        serie.save()
        count_after = Serie.objects.count()
        self.assertLess(count_before, count_after)
        self.assertEqual(serie.note_set.count(), 0)

    # Note model tests
    def test_create_and_save_new_note(self):
        serie = Serie(title="Notes to future self")
        serie.save()
        note = Note(content="My first note. Here is to a great day", serie=serie)
        self.assertTrue(note)
        self.assertEqual(note.serie, serie)
        self.assertEqual(note.content, "My first note. Here is to a great day")
        count_before = Note.objects.count()
        note.save()
        count_after = Note.objects.count()
        self.assertLess(count_before, count_after)
        self.assertEqual(serie.note_set.count(), count_after)
