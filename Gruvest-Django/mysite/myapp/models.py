from django.db import models

# Create your models here.
class PostModel(models.Model):
    header = models.CharField(max_length = 100)
    post = models.CharField(max_length = 240)
    UpVote = models.IntegerField(default = 1)
    DownVote = models.IntegerField(default = 1)

    def __str__(self):
        return self.post

    def GetTotalVotes(self):
        return self.UpVote - self.DownVote
    
    def AddUpVote(self):
        self.UpVote += 1
        return self.UpVote

   