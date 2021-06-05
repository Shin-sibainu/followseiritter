from django.shortcuts import render
import tweepy
from datetime import datetime, timedelta
import pprint
import json
import time

consumer_key = 'b6iBIHJYu8kEM3RqFISRw4XAW'
consumer_secret = 'Y7RzFAgmLLKU9KzDzL5OcLjmfHbUI7Alz7drbYk7soJOMySfLt'
access_token = '1327957216117227521-gr1zdKzpwaVoPm9uXbY1Fd9097HtD2'
access_token_secret = 'rxEokEDi2ZrjRu0JPMt1rXDqiAc1zCsPomTVUFqcZO315'
  
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#friends_search_count = 200
friends_ids_search_count = 15
deadacount_definision = 30

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

# 死んでるアカウントを表示する関数
def deadacountView(request): 
  if request.method == 'POST':
    username = request.POST['username']
    friends_ids = api.friends_ids(screen_name=username, count=friends_ids_search_count) #クライアントがフォローしているユーザーのidをいくつか取得する。
    
    deadacount = []
    aliveacount = []

    for friend_id in friends_ids: #フォローしているユーザーIDを1つずつ取り出す。
      friend = api.get_user(friend_id) #取り出したUserIDから1つずつUserオブジェクトを探しにいく。
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
    
    print(len(deadacount)+len(aliveacount))
  return render(request, 'deadacount.html', context)


def htmlpraView(request):
  return render(request, 'htmlpra.html')