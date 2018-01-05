from selenium import webdriver
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
        self.fail('Finich the test!')

        # He is  invited to create a serie straight a way

        # He types " Notes to future self" into a text box

        # When he hits enter, the page updates with a new listing
        # "Notes to future self" as a new serie

        # There is a text box inviting him to add a note to the serie

        # He enters, " My first note" and presses enter

        # Now the serie has a single note : "My first Note, Date"

        # There is still a text box inviting him to add another note to the serie

        # He enters, " That was easy" and presses enter

        # The page updates again, and now both notes are listed

        # Jodom wonders whether the site will remember his notes

        # Then he sees that the site generated a uniqe URL for him
        # -- there is some explanatory text to that effect

        # He visits that URL. His notes are still there

        # Satisfied, he goes back to sleep

if __name__ == '__main__':
    unittest.main()
