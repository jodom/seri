from selenium import webdriver
import unittest

class NewNotesTest(unittest.TestCase):

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
        self.fail('Finich the test!')

        # He is  invited to enter a note straight a way

        # He types " My first note" into a text box

        # When he hits enter, the page updates with a new listing
        # "My first note, date" as an item in the seris

        # There is still a text box inviting him to add a new note

        # He enters, " That was easy" and presses enter

        # The page updates again, and now both items are listed

        # Jodom wonders whether the site will remember his notes

        # Then he sees that the site generated a uniqe URL for him -- ther is some explanatory text to that effect

        # He visits that URL. His notes are still there

        # Satisfied, he goes back to sleep

if __name__ == '__main__':
    unittest.main()
