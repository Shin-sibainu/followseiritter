from django.urls import path
from .views import homeView, tweetView, followersView, myfriendsView, deadacountView, htmlpraView
from .views import deadacountView2, getTwitterApiDataView, ajaxPra, getDataPra

urlpatterns = [
  path('', homeView, name='home'),
  path('tweet/', tweetView, name='tweet'),
  path('friends/', myfriendsView, name='friends'),
  path('followers/', followersView, name='followers'),
  path('deadacount/', deadacountView, name='deadacount'),
  path('deadacount2/', deadacountView2, name='deadacount2'),
  path('htmlpra/', htmlpraView, name='htmlpra'),
  path('twitter_api_data/', getTwitterApiDataView, name='twitter_api_data'),
  path('ajaxpra/', ajaxPra, name='ajaxpra'),
  path('getDataPra/', getDataPra, name='getDataPra'),
  #path('getClickCount', getClickCount, name='getClickCount')
]