from django.urls import path
from . import views
from django.contrib.auth import views as authViews
from chartjs import views as chartViews

urlpatterns = [
    path('', views.index, name= 'main'),
    path('post/', views.PitchCreator.as_view(), name='postPitch'),
    path('list/', views.PitchList.as_view(), name='pitchList'),
    path('user/<int:pk>', views.UserDetail.as_view(), name='pitchDetail'), # PROBLEM! DOESN'T LIKE IT WHEN I CHANGE 'pitchDetail' TO 'userDetail'
    path('like/<int:pk>', views.upVoteView, name='upVotePost'),
    path('dislike/<int:pk>', views.downVoteView, name='downVotePost'),
    path('fund/<int:pk>', views.AddFunds.as_view(), name='addFunds'),
    path('comment/<int:pk>', views.CommentCreator.as_view(), name='postComment'),
    path('login/', authViews.LoginView.as_view()),
    path('register/', views.register),
    path('logout/', views.logout_view),
    path('subscribe/<int:pk>', views.subscribeView, name='sub'),
    path('cost/', views.sortedCost, name="sortedCost"),
    path('date/', views.sortedDate, name="sortedDate"),
    path('chartjs/', chartViews.HomeView.as_view(), name='chart'),
    path('api', chartViews.ChartData.as_view(), name='chartData'),
<<<<<<< HEAD
    path('main', views.main, name='MAIN'),
]
=======
]

>>>>>>> 5f9295ad2221a22d4be58b61ed63dc506ded1a71
