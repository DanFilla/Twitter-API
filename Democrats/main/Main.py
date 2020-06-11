import tweepy
import threading
import logging
from classes.StreamClass import MyStreamListener

consumer_key = "O440GKDKaFDlouDj5nutK0d6N"
consumer_secret = "byeBjTsocrXgNoBW8XMv4p1jUGVU6SUTMv1UhzQAfaSLFYV1a4"

key = "1083113049568038924-lMexUYQA0r06vwunKoSwhufa9QG4Es"
secret = "jIT1NclZ4zd8nY5IA2hc7MabBPrussrECVDMtZrtBYcaW"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)

myStreamListener = MyStreamListener()

myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

dem_id_list = []

#parse through senator data file to get twitter user id
with open("../data/dem_data/dem_ids.txt", "r") as data:
    for line in data:
        line = line.split()
        for word in line:
            try:
                int(word)
                dem_id_list.append(str(word))
            except ValueError:
                continue
try:
    myStream.filter(dem_id_list)
except:


