from django.test import TestCase
from . import models
# Create your tests here.

class PitchTestCase(TestCase):
    def setUp(self):
        models.PostModel.objects.create(header="test", post="hi", cost=20, upVotes=20, downVotes=2)
       
    def test_pitch_creation(self):
        testPitch =  models.PostModel.objects.get(header="test")
        self.assertEqual(testPitch.getTotalVotes(), 18)
