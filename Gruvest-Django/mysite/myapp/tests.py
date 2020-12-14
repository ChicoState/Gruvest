from django.test import TestCase, Client
from django.test.client import RequestFactory

from django.contrib.auth.models import User
from . import forms
from . import models
from . import views

# Create your tests here.

class PitchTestCase(TestCase):
    
    def setUp(self):
        self.factory = RequestFactory()
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        client = Client()
        client.login(username='testuser', password='12345')
        models.UserModel.objects.create(header="test", post="hi", cost=20, upVotes=20, downVotes=2, author=user)
       
    def test_pitch_creation(self):
        testPitch =  models.UserModel.objects.get(header="test")
        self.assertEqual(testPitch.getTotalVotes(), 18)

    def test_pitch_creation_cost(self):
        testPitch =  models.UserModel.objects.get(header="test")
        self.assertEqual(testPitch.getCost(), 20)


    def test_pitch_detail(self):
        testPitch =  models.UserModel.objects.get(header="test")
        request = self.client.get('/user/' + str(testPitch.pk))
        self.assertEqual(request.status_code, 302)

    def test_add_funds_form_Valid(self):
        form = forms.AddFundsForm(data={'funds': 5})
        self.assertTrue(form.is_valid())

    def test_add_funds_form_Invalid_Negative(self):
        form = forms.AddFundsForm(data={'funds': -5})
        self.assertFalse(form.is_valid())

    def test_add_funds_form_Invalid_NotInt(self):
        form = forms.AddFundsForm(data={'funds': 5.7})
        self.assertFalse(form.is_valid())

    def test_add_comment_form_Valid(self):
        form = forms.PostCommentForm(data={'comment': "cool idea!"})
        self.assertTrue(form.is_valid())

    def test_add_comment_form_Invalid(self):
        form = forms.PostCommentForm(data={'comment': "fufvaafzopplaimpkyfmdxjdcollrwxilcfawwensmlonukgvkegborulnmhgmsexnrqiilecvvelghldqveautoeabxgudfbrtkiltsnzvevmyvjuhpeerdrzvtmgfffvmplektkrertpbvqymldxqrqqmvwdhmrqvtvsptjbcdwapjwoikdvhfgzkwbrlyftudrfdfyagmpljjqghudsnrvuhzcbmunfwwwpzvnvlqmicniajcjyqlmrjcaqyqcnhvrsxvlufihhnfszuocksxghndykvmdfalzsdplfmystygojpnomollqemsspczsxjwdooqnzckoigmwquioaqmoojocsussoejikqyhgrbafimpydarrkdgdhwfknhkzsackleodhlxmcwdjigmrybakagwsdqstxqywwcxkndcnhxegavvvnprooalrvsfahfyupubamxcgnnjwpuaqqtczfphowbfypuflejroiapxkftmhnvniqoriwbrjqfuaehxdvuqprlaplcflnhmezpauambpldfuwpqqsowjawrnpdqullzzvuiqp"})
        self.assertFalse(form.is_valid())

    def test_post_pitch_form_Valid(self):
        form = forms.PostPitchForm(data={"header": "hi", "post": "great test", 'cost': 50})
        self.assertTrue(form.is_valid())
    
    def test_post_pitch_form_Invalid(self):
        form = forms.PostPitchForm(data={"header": "hi", "post": "great test", 'cost': -50})
        self.assertFalse(form.is_valid())

    def test_upvote_happy(self):
        testPitch =  models.UserModel.objects.get(header="test")
        request = self.factory.post('/like/' + str(testPitch.pk))
        request.user = User.objects.get(username="testuser")
        views.upVoteView(request, testPitch.pk)
        self.assertEqual(testPitch.getTotalVotes(), 19)

    def test_upvote_undo(self):
        testPitch =  models.UserModel.objects.get(header="test")
        request = self.factory.post('/like/' + str(testPitch.pk))
        request.user = User.objects.get(username="testuser")
        views.upVoteView(request, testPitch.pk)
        views.upVoteView(request, testPitch.pk)
        self.assertEqual(testPitch.getTotalVotes(), 18)

    def test_downvote_happy(self):
        testPitch =  models.UserModel.objects.get(header="test")
        request = self.factory.post('/dislike/' + str(testPitch.pk))
        request.user = User.objects.get(username="testuser")
        views.downVoteView(request, testPitch.pk)
        self.assertEqual(testPitch.getTotalVotes(), 17)

    def test_pitch_creation_page(self):
        request = self.client.get('/post/')
        self.assertEqual(request.status_code, 302)

    def test_index_page(self):
        request = self.client.get('')
        self.assertEqual(request.status_code, 200)

    def test_sort_byCost_page(self):
        request = self.client.get('/cost/')
        self.assertEqual(request.status_code, 200)

    def test_sort_byDate_page(self):
        request = self.client.get('/date/')
        self.assertEqual(request.status_code, 200)

    def test_subscribe_button(self):
        user = User.objects.create(username='testuser2')
        user.set_password('12345')
        user.save()
        testPitch =  models.UserModel.objects.get(header="test")
        request = self.factory.post('/subscribe/' + str(testPitch.pk))
        request.user = User.objects.get(username="testuser2")
        views.subscribeView(request, testPitch.pk)
        response = self.client.get('/subscribe/' + str(testPitch.pk))
        self.assertEqual(response.status_code, 302)



    