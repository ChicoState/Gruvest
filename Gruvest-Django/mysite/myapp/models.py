from django.db import models

# Create your models here.
class PostModel(models.Model):
    header = models.CharField(max_length = 100)
    post = models.CharField(max_length = 240)
    vote = models.IntegerField(default = 1)

    def __str__(self):
        return self.post
