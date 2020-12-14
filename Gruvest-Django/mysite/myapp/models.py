from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

'''Post Model is now the User Page'''
class UserModel(models.Model):
    header = models.CharField(max_length=100)
    post = models.CharField(max_length=5000)

    # ForeignKey is M:1
    # Does this mean we design StocksModel to contain one value per field?
    #stocks = models.ForeignKey(StocksModel, on_delete=models.CASCADE) # what does CASCADE mean?

    # how to go about function that calculates portfolio?

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


# Contains stocks
class StocksModel(models.Model):
    ticker = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True)
    pitcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stock_user')
    #category = models.CharField(max_length=4, choices=options, default=1)
    #closingPrice = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)

'''
# Contains list of all tracked stocks for pitcher
class TrackedStocksModel(models.Model):
    pitcher = models.ForeignKey(UserModel, on_delete=models.CASCADE) # 1:1 with pitcher
    data = models.ManyToManyField(StocksModel)
    description = models.CharField(max_length=100, default="")

    # ENABLE JSON IN SQLITE
    #data = models.JSONField(null=True)

    # changes each time category is changed
    date = models.DateTimeField(auto_now_add=True)

    # tracks accuracy of stock % inc/dec
    #accuracy = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    
    BUY = 0
    HOLD = 1
    SELL = 2
    
    options = [
        (0, 'BUY'),
        (1, 'HOLD'),
        (2, 'SELL'),
    ]
    category = models.CharField(max_length=4, choices=options, default=1)

    def getOptions(self):
        return self.options
'''

class CommentModel(models.Model):
    comment = models.CharField(max_length=240)
    post = models.ForeignKey('UserModel', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    def get_absolute_url(self):
        return HttpResponseRedirect(reverse_lazy("main"))

class UpvoteModel(models.Model):
    upvoter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='upvote_user')
    upvotedPost = models.ForeignKey('UserModel', on_delete=models.CASCADE, related_name='upvoted_post')

class DownvoteModel(models.Model):
    downvoter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='downvote_user')
    downvotedPost = models.ForeignKey('UserModel', on_delete=models.CASCADE, related_name='downvoted_post')

class PurchaseModel(models.Model):
    purchaser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchase_user')
    purchasedPost = models.ForeignKey('UserModel', on_delete=models.CASCADE, related_name='purchased_post')

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