from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your models here.
class PostModel(models.Model):
    header = models.CharField(max_length=100)
    post = models.CharField(max_length=240)
    upVotes = models.IntegerField(default=0)
    downVotes = models.IntegerField(default=0)
    cost = models.PositiveIntegerField(default=1)

    def __str__(self):
        return (self.header + "\n" + self.post)
    
    def getUpVotes(self):
        return self.upVotes
    
    def getDownVotes(self):
        return self.downVotes

    def getTotalVotes(self):
        return self.upVotes - self.downVotes
    
    def get_absolute_url(self):
        return HttpResponseRedirect(reverse("main"))

class CommentModel(models.Model):
    comment = models.CharField(max_length=240)
    post = models.ForeignKey('PostModel', on_delete=models.CASCADE, related_name='comments')
    
    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return HttpResponseRedirect(reverse_lazy("main"))

class UpvoteModel(models.Model):
    upvoter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='upvote_user')
    upvotedPost = models.ForeignKey('PostModel', on_delete=models.CASCADE, related_name='upvoted_post')

class DownvoteModel(models.Model):
    downvoter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='downvote_user')
    downvotedPost = models.ForeignKey('PostModel', on_delete=models.CASCADE, related_name='downvoted_post')

class PurchaseModel(models.Model):
    purchaser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchase_user')
    purchasedPost = models.ForeignKey('PostModel', on_delete=models.CASCADE, related_name='purchased_post')

class CatcherModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    funds = models.PositiveIntegerField(default = 0, verbose_name= 'Add amount')