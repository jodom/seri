from django.test import TestCase

# Create your tests here.

class SmokeTest(TestCase):

    def test_quick_math(self):
        self.assertEqual(2+2-1, 3)
