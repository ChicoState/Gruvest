from django.test import TestCase, Client
from django.contrib.auth.models import User
from . import models
# Create your tests here.

class PitchTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='testuser', password='12345')
        models.UserModel.objects.create(header="test", post="hi", cost=20, upVotes=20, downVotes=2, author=user)
       
    def test_pitch_creation(self):
        testPitch =  models.UserModel.objects.get(header="test")
        self.assertEqual(testPitch.getTotalVotes(), 18)
