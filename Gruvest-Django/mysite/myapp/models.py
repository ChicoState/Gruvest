from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class PostModel(models.Model):
    header = models.CharField(max_length=100)
    post = models.CharField(max_length=240)
    #UpVote = models.ManyToManyField(User, related_name='pitchUp')
    upVotes = models.IntegerField(default=0)
    #DownVote = models.ManyToManyField(User, related_name='pitchDown')
    downVotes = models.IntegerField(default=0)

    def __str__(self):
        return self.post
    
    def getUpVotes(self):
        return self.upVotes
    
    def getDownVotes(self):
        return self.downVotes

    def getTotalVotes(self):
        return self.upVotes - self.downVotes
    '''
    def addUpVote(self):
        self.upVote += 1
        return self.UpVote

    def addDownVote(self):
        self.downVote += 1
        return self.DownVote
    '''

class CommentModel(models.Model):
    comment = models.CharField(max_length=240)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comments')
    
    def __str__(self):
        return self.comment
