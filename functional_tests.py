from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewSerieTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_serie_and_see_it_later(self):
        # Jodom has been intospecting a lot lately
        # He has bult an app to capture his thoughts in the form of short notes
        # So he goes home and checks the homepage

        self.browser.get('http://localhost:8000')

        # He notices that the page title and header mention Seris - the note taking app
        self.assertIn('Seris, a note a day', self.browser.title)

        header = self.browser.find_element_by_tag_name('h1').text

        self.assertIn('Seris', header)


        # He is  invited to create a serie straight a way
        seriebox = self.browser.find_element_by_id('id_new_serie')
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
        notebox.send_keys('My first note').send_keys(Keys.ENTER)
        table = self.browser.find_element_by_id('id_notes_table')

        # Now the serie has a single note : "My first Note, Date"
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(any(row.text == 'My first note') for row in rows)

        # There is still a text box inviting him to add another note to the serie
        # He enters, " That was easy" and presses enter
        self.fail('Finich the test!')

        # The page updates again, and now both notes are listed

        # Jodom wonders whether the site will remember his notes

        # Then he sees that the site generated a uniqe URL for him
        # -- there is some explanatory text to that effect

        # He visits that URL. His notes are still there

        # Satisfied, he goes back to sleep

if __name__ == '__main__':
    unittest.main()
