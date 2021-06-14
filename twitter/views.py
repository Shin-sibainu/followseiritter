from django.http import JsonResponse
from django.shortcuts import render
import tweepy
from datetime import datetime, timedelta
import sys
from django.http import QueryDict, HttpResponse
import json

consumer_key = 'b6iBIHJYu8kEM3RqFISRw4XAW'
consumer_secret = 'Y7RzFAgmLLKU9KzDzL5OcLjmfHbUI7Alz7drbYk7soJOMySfLt'
access_token = '1327957216117227521-gr1zdKzpwaVoPm9uXbY1Fd9097HtD2'
access_token_secret = 'rxEokEDi2ZrjRu0JPMt1rXDqiAc1zCsPomTVUFqcZO315'
  
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

friends_ids_search_count = 10
friends_ids_search_count_click = 30
deadacount_definision = 1

def homeView(request):
  return render(request, 'home.html')

def tweetView(request):
  #home.htmlで打ち込んだテキスト内容をツイートしたい。
  if request.method == 'POST':
    tweet = request.POST['tweet']
    api.update_status(tweet)
    context = {
     'tweet': tweet
    }
  return render(request, 'tweet.html', context)

#自分のフォローしているユーザーを列挙する。
def myfriendsView(request):
  friends = api.friends()#自分がフォローしているUserオブジェクトをリストで保持している。
  
  friends_list = []
  
  for friend in friends:
    friend_name = friend.name #フォローしているユーザー名を1つずつ取得する。
    friends_list.append(friend_name)#リストにフレンドの名前を1つずつ格納する。 

  context = {
    'friends_list': friends_list
   }

  return render(request, 'myfriends.html', context)

#usernameを入力するとそのユーザーをフォローしているユーザーを10人まで列挙する。
def followersView(request):
  if request.method == 'POST':
    print(request.POST)
    username = request.POST['username']
    user_info = api.get_user(username)#打ち込んだユーザー名からそのユーザーオブジェクトを取得する。
    followers = user_info.followers(count=1)

    followers_list = []
    for follower in followers:
      follower_name = follower.name
      followers_list.append(follower_name)

    context = {
      'followers_list': followers_list
    }
  return render(request, 'followers.html', context)

def htmlpraView(request):
  return render(request, 'htmlpra.html')

# 死んでるアカウントを表示する関数
def deadacountView(request): 
  if request.method == 'GET':
    username = request.GET['username']
    friends_ids = api.friends_ids(screen_name=username, count=friends_ids_search_count) #クライアントがフォローしているユーザーのidをいくつか取得する。
    
    deadacount = []
    aliveacount = []

    for friend_id in friends_ids: #フォローしているユーザーIDを1つずつ取り出す。
      #-----------------------------------------(遅い)
      friend = api.get_user(friend_id) #取り出したUserIDから1つずつUserオブジェクトを探しにいく。
      #-----------------------------------------（遅い）
      try:
        friend_statusObj = api.user_timeline(friend.id, count=1) #フォローしてるUserIDのタイムラインの最新投稿（Statusオブジェクト）を取得。
      except tweepy.TweepError as e:
        if e.reason == 'Not authorized.':
          print('鍵垢の人がいました。')
      
      setattr(friend, 'profile_url', 'https://twitter.com/{}'.format(friend.screen_name)) #Userオブジェクトに属性を付与する。

      for friend_status in friend_statusObj:
        new_tweet_created_at = friend_status.created_at #各々ユーザーの最新投稿の日時を取得している。
        if datetime.now() - new_tweet_created_at > timedelta(days=deadacount_definision): #最新の投稿が半年間更新されていなかったら。 
          deadacount.append(friend) #死んでるUserオブジェクトのリスト
        else:
          aliveacount.append(friend)

    context = {
       'deadacount_list': deadacount,
       'aliveacount_list': aliveacount
     }
  return render(request, 'deadacount.html', context)


def deadacountView2(request):
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
        print(ae)
      if datetime.now() - new_tweet_created > timedelta(days=deadacount_definision):
        deadacount.append(friendObj)
      else:
        aliveacount.append(friendObj)  
    context = {
      'deadacount_list': deadacount,
      'aliveacount_list': aliveacount
    }
    
  return render(request, 'deadacount2.html', context)

#TwitterAPIからscreen_nameの情報をとってくる。
def getTwitterApiDataView(request):
  click_count = 0
  #Ajaxで送られてきた変数を受け取る。
  if request.method == 'POST':
    friends_ids_list = []
    friends_ids_list_10 = []
    friends_ids_list_20 = []
    friends_ids_list_30 = []

    deadacount = {}
    aliveacount = {}
    deadacountlist = []
    aliveacountlist = []

    friends_ids = api.friends_ids(screen_name='juvenile_1225', count=friends_ids_search_count_click)
    #id100件毎のリストを作る。
    for friend_id in friends_ids:
      if(len(friends_ids_list_10) <= 10):
        friends_ids_list_10.append(friend_id )
      if(len(friends_ids_list_10) >= 11 and len(friends_ids_list_20) < 10):
        friends_ids_list_20.append(friend_id)
      if(len(friends_ids_list_20) >= 10):
        friends_ids_list_30.append(friend_id)
    friends_ids_list.append(friends_ids_list_10)
    friends_ids_list.append(friends_ids_list_20)
    friends_ids_list.append(friends_ids_list_30)

    dic = QueryDict(request.body, encoding='utf-8')
    click_count = dic.get('clickcount_for_next_list')
    print(click_count)

    #print(click_count)
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
    return JsonResponse({'deadacount_list':deadacountlist, 'aliveacount_list':aliveacountlist}, safe=False) 



#------------ここからは練習---------------
  #データ取得練習
  def getDataPra(request):
    if request.method == 'POST': 
      #Querydictでしか受け取れない。 
      dic = QueryDict(request.body, encoding='utf-8')
      click_count_data = dic.get('clickcount_for_next_list')
      #Json形式に置き換えている。
      ret = json.dumps({'clickcount_for_next_list': click_count_data})
      return HttpResponse(ret, content_type='application/json')

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




