from django.http import JsonResponse
from django.shortcuts import render
import tweepy
from datetime import datetime, timedelta
from django.http import QueryDict, HttpResponse
import json

consumer_key = 'b6iBIHJYu8kEM3RqFISRw4XAW'
consumer_secret = 'Y7RzFAgmLLKU9KzDzL5OcLjmfHbUI7Alz7drbYk7soJOMySfLt'
access_token = '1327957216117227521-gr1zdKzpwaVoPm9uXbY1Fd9097HtD2'
access_token_secret = 'rxEokEDi2ZrjRu0JPMt1rXDqiAc1zCsPomTVUFqcZO315'
  
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

friends_ids_search_count = 100
friends_ids_search_count_click = 5000
deadacount_definision = 90

def homeView(request):
  return render(request, 'home.html')


def deadacountView(request):
  if request.method == "GET":
    screen_name = request.GET["screen_name"]
    
    deadacount = []
    aliveacount = []

    friends_ids = api.friends_ids(screen_name=screen_name, count=friends_ids_search_count)
    friendsObj = api.lookup_users(user_ids=friends_ids) #最大100まで

    for friendObj in friendsObj:
      try:
        new_tweet_created = friendObj.status.created_at
        setattr(friendObj, 'profile_url', 'https://twitter.com/{}'.format(friendObj.screen_name))
      except AttributeError as ae:
        pass
      if datetime.now() - new_tweet_created > timedelta(days=deadacount_definision):
        deadacount.append(friendObj)
      else:
        aliveacount.append(friendObj)  
    context = {
      'deadacount_list': deadacount,
      'aliveacount_list': aliveacount
    }
    
  return render(request, 'deadacount.html', context)

#TwitterAPIからscreen_nameの情報をとってくる。
def getTwitterApiDataView(request):
  click_count = 0
  isOverList = False
  #Ajaxで送られてきた変数を受け取る。
  if request.method == 'POST':
    friends_ids_list = []
    deadacount = {}
    aliveacount = {}
    deadacountlist = []
    aliveacountlist = []

    dic = QueryDict(request.body, encoding='utf-8')
    click_count = dic.get('clickcount_for_next_list')
    screen_name = dic.get('screen_name_data')
    #(Todo)1度で5000件取得するから呼び出すのは最初の1クリックだけで良い。
    friends_ids = api.friends_ids(screen_name=screen_name, count=friends_ids_search_count_click)
    #id100件毎のリストを作る。
    friends_ids_list = [friends_ids[i:i+100] for i in range(0,friends_ids_search_count_click, 100)]
    try:
      friendsObj = api.lookup_users(user_ids=friends_ids_list[int(click_count)]) #最大100まで

      for friendObj in friendsObj:
        try:
          new_tweet_created = friendObj.status.created_at
          setattr(friendObj, 'profile_url', 'https://twitter.com/{}'.format(friendObj.screen_name))
          if datetime.now() - new_tweet_created > timedelta(days=deadacount_definision):
            try:
              deadacount['name'] = friendObj.name
              deadacount['screen_name'] = friendObj.screen_name
              deadacount['profile_url'] = friendObj.profile_url
              deadacount['profile_image_url_https'] = friendObj.profile_image_url_https
              deadacountlist.append(deadacount.copy())
            except AttributeError as ae:
              pass
          else:
            try:
              aliveacount['name'] = friendObj.name
              aliveacount['screen_name'] = friendObj.screen_name
              aliveacount['profile_url'] = friendObj.profile_url
              aliveacount['profile_image_url_https'] = friendObj.profile_image_url_https
              aliveacountlist.append(aliveacount.copy())
            except AttributeError as ae:
              pass
        except AttributeError as ae:
            pass
    except tweepy.error.TweepError as tet:
      #リストがありませんとHTMLに出力したい。
      print(tet.response)
      isOverList = True
      return JsonResponse({'isOverList': isOverList}, safe=False) 
    return JsonResponse({'deadacount_list':deadacountlist, 'aliveacount_list':aliveacountlist}, safe=False) 



#------------ここからは練習用---------------
#ボタンカウントを画面に表示する練習
def ajaxPra(request):
  return render(request, 'ajaxpra.html', {})

#データ取得練習
def getDataPra(request):
  if request.method == 'POST': 
    #Querydictでしか受け取れない。 
    dic = QueryDict(request.body, encoding='utf-8')
    click_count_data = dic.get('click_count')
    #Json形式に置き換えている。
    ret = json.dumps({'click_count': click_count_data})
    return HttpResponse(ret, content_type='application/json')




