from django.urls import path
from .views import homeView, deadacountView, getTwitterApiDataView

urlpatterns = [
  path('', homeView, name='home'),
  path('deadacount/', deadacountView, name='deadacount'),
  path('twitter_api_data/', getTwitterApiDataView, name='twitter_api_data'),
]