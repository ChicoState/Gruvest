from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'main'),
    path('post/', views.PitchCreator.as_view(), name='postPitch'),
    path('like/<int:pk>', views.upVoteView, name='upVotePost'),
    path('dislike/<int:pk>', views.downVoteView, name='downVotePost'),
    #path('comment/<int:pk>', views.commentView, name='commentPost')
]