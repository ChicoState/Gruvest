from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'main'),
    path('like/<int:pk>', views.UpVoteView, name= 'UpVotePost'),
    path('dislike/<int:pk>', views.DownVoteView, name= 'DownVotePost'),
]