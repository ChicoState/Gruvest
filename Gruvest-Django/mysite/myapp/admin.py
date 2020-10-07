from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.PostModel)
admin.site.register(models.CommentModel)
admin.site.register(models.UpvoteModel)
admin.site.register(models.DownvoteModel)