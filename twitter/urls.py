from django.urls import path
from .views import homeView, tweetView, followersView, myfriendsView, deadacountView, htmlpraView

urlpatterns = [
  path('', homeView, name='home'),
  path('tweet/', tweetView, name='tweet'),
  path('friends/', myfriendsView, name='friends'),
  path('followers/', followersView, name='followers'),
  path('deadacount/', deadacountView, name='deadacount'),
  path('htmlpra/', htmlpraView, name='htmlpra')
]