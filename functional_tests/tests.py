from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewSerieTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def create_new_note(self, text):
        ''' type and save a note '''
        notebox = self.browser.find_element_by_id('id_new_note')
        self.assertEqual(notebox.get_attribute('placeholder'), 'New note')

        notebox.send_keys(text)
        notebox.send_keys(Keys.ENTER)

    def confirm_serie_title(self, text):
        ''' confirm the current serie title '''
        title = self.browser.find_element_by_id('id_serie_title')
        self.assertEqual(title.text, text)

    def lookup_a_note_in_a_serie(self, text):
        ''' confirm the existence of a note in a serie '''
        notes_list = self.browser.find_element_by_tag_name('ul')
        notes = notes_list.find_elements_by_tag_name('li')

        self.assertIn(text, [note.content for note in notes])
        self.assertTrue(any(note.content == text for note in notes))

    def test_can_save_a_quick_note_and_see_it_later(self):
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

        # There is a box inviting Jodom to create a note straight away
        # He types 'This is a quick note' and presses ENTER
        self.create_new_note('This is a quick note')
        
        # The page updates and he sees a page with the heading 'My Notes' and his note listed under it
        jodom_default_serie_url = self.browser.current_url
        self.assertRegex(jodom_default_serie_url, '/serie/.+')

        self.confirm_serie_title('My Notes')

        self.lookup_a_note_in_a_serie('This is a quick note')

        # There is a text box inviting him to add another note to the serie
        # He enters, " My first note" and presses enter
        self.create_new_note('My second note')

        # Now the serie has a single note : "My first Note"
        self.lookup_a_note_in_a_serie('My second note')

        # There is still a text box inviting him to add another note to the serie
        # He enters, " That was easy" and presses enter
        self.create_new_note('That was easy')

        # The page updates again, and now both notes are listed under the quick note
        self.lookup_a_note_in_a_serie('This is a quick note')
        self.lookup_a_note_in_a_serie('My second note')
        self.lookup_a_note_in_a_serie('That was easy')

        # Jodom recommend the app to his friend Liz, who comes along to the site from a different browser
        # # this prevents cookie and session data transfer
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # Liz visits the homepage. There is no sign of Jodoms notes and Seris
        self.browser.get(self.live_server_url)

        page = self.browser.find_element_by_tag_name('body')
        self.assertNotIn('This is a quick note', page.text)
        self.assertNotIn('My second note', page.text)
        self.assertNotIn('That was easy', page.text)

        # Liz decides to save a new note for herself
        self.create_new_note('Buy milk after class')

        # She gets her own unique URL
        liz_default_serie_url = self.browser.current_url
        self.assertRegex(liz_default_serie_url, '/serie/.+')
        self.assertNotEqual(jodom_default_serie_url, liz_default_serie_url)

        # To confirm Jodom's notes are not showing
        page = self.browser.find_element_by_tag_name('body')
        self.confirm_serie_title('My Notes')
        self.assertNotIn('This is a quick note', page.text)
        self.assertNotIn('My second note', page.text)
        self.assertNotIn('That was easy', page.text)
