from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewSerieTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def lookup_a_note_in_a_serie(self, text):
        notes_list = self.browser.find_element_by_tag_name('ul')
        notes = notes_list.find_elements_by_tag_name('li')

        self.assertIn(text, [note.content for note in notes])
        self.assertTrue(any(note.content == text for note in notes))

    def test_can_start_a_serie_and_see_it_later(self):
        # Jodom has been intospecting a lot lately
        # He has bult an app to capture his thoughts in the form of short notes
        # So he goes home and checks the homepage

        self.browser.get(self.live_server_url)

        # He notices that the page title and header mention Seris - the note taking app
        self.assertIn('Seris', self.browser.title)

        header = self.browser.find_element_by_id('id_header').text
        self.assertEqual('Seris', header)

        # Below the header is a catchphrase, 'a note a day'
        sub_header = self.browser.find_element_by_id('id_sub_header').text
        self.assertEqual('a note a day', sub_header)

        # Under the catchphrase, there is a link inviting him to create a serie
        new_serie_link = self.browser.find_element_by_id('id_new_serie')

        # He clicks on it and is taken to a new page where he can create a serie
        new_serie_link.send_keys(Keys.ENTER)

        # He is  invited to create a serie straight a way
        seriebox = self.browser.find_element_by_id('id_title_input')
        self.assertEqual(seriebox.get_attribute('placeholder'), 'Create a new Serie')

        # He types "Notes to future self" into a text box
        seriebox.send_keys('Notes to future self')

        # When he hits enter, the page updates with a new listing
        # "Notes to future self" as a new serie
        seriebox.send_keys(Keys.ENTER)

        # The new Serie is created, with a page showing its title now being displayed
        title = self.browser.find_element_by_id('id_serie_title')
        self.assertEqual(title.text, 'Notes to future self')

        # There is a text box inviting him to add a note to the serie
        notebox = self.browser.find_element_by_id('id_new_note')
        self.assertEqual(notebox.get_attribute('placeholder'), 'New note')

        # He enters, " My first note" and presses enter
        notebox.send_keys('My first note')
        notebox.send_keys(Keys.ENTER)

        # Now the serie has a single note : "My first Note"
        self.lookup_a_note_in_a_serie('My first note')

        # There is still a text box inviting him to add another note to the serie
        # He enters, " That was easy" and presses enter
        notebox.send_keys('That was easy')
        notebox.send_keys(Keys.ENTER)

        # The page updates again, and now both notes are listed
        self.lookup_a_note_in_a_serie('My first note')
        self.lookup_a_note_in_a_serie('That was easy')

        # Jodom wonders whether the site will remember his notes
        self.fail('Finich the test!')

        # Then he sees that the site generated a uniqe URL for him
        # -- there is some explanatory text to that effect

        # He visits that URL. His notes are still there

        # Satisfied, he goes back to sleep
