from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class PostModel(models.Model):
    header = models.CharField(max_length=100)
    post = models.CharField(max_length=5000)
    upVotes = models.IntegerField(default=0)
    downVotes = models.IntegerField(default=0)
    cost = models.PositiveIntegerField(default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (self.header + "\n" + self.post)
    
    def getUpVotes(self):
        return self.upVotes
    
    def getDownVotes(self):
        return self.downVotes

    def getTotalVotes(self):
        return self.upVotes - self.downVotes
     
    def getCost(self):
        return self.cost  

    def getDate(self):
        return self.published_on
    
    def get_absolute_url(self):
        return HttpResponseRedirect(reverse("main"))

class CommentModel(models.Model):
    comment = models.CharField(max_length=240)
    post = models.ForeignKey('PostModel', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_on = models.DateTimeField(auto_now_add=True)

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

    def checkUser(self):
        if(User == self.purchaser):
            return True
        else:
            return False

class CatcherModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    funds = models.PositiveIntegerField(default = 0, verbose_name= 'Add amount')

    def __str__(self):
        return str(self.user)

#function comes from this tutorial: https://rb.gy/8mu15h
@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        CatcherModel.objects.create(user=instance)
    instance.catchermodel.save()

class SubscribeModel(models.Model):
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subcribe_user')
    pitcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pitcher_user')

    def __str__(self):
        return str(self.pitcher)