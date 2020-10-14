from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'main'),
    path('post/', views.PitchCreator.as_view(), name='postPitch'),
    path('list/', views.PitchList.as_view(), name='pitchList'),
    path('pitch/<int:pk>', views.PitchDetail.as_view(), name='pitchDetail'),
    path('like/<int:pk>', views.upVoteView, name='upVotePost'),
    path('dislike/<int:pk>', views.downVoteView, name='downVotePost'),
]