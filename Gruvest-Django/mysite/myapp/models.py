from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class PostModel(models.Model):
    header = models.CharField(max_length = 100)
    post = models.CharField(max_length = 240)
    UpVote = models.ManyToManyField(User, related_name='pitchUp')
    DownVote = models.ManyToManyField(User, related_name='pitchDown')

    def __str__(self):
        return self.post
    
    def GetUpVotes(self):
        return self.UpVote.count()

    def GetTotalVotes(self):
        return self.UpVote.count() - self.DownVote.count()
    
    def AddUpVote(self):
        self.UpVote += 1
        return self.UpVote

    def AddDownVote(self):
        self.DownVote += 1
        return self.DownVote
    

