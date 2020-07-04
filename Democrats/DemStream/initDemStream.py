import sys
sys.path.append('/Users/dan/Desktop/Twitter-API/keys')
import tweepy
import threading
import logging
import datetime
import time
import os
from secret_keys import *
from Democrats.DemStream.classes.StreamClass import MyStreamListener

logging.basicConfig(filename="logging-files/dem_logs.log")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)

myStreamListener = MyStreamListener()

myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

dem_id_list = []

# with open("Democrats/data/dem_data/dem_status_data.csv", "a") as csv_file:
    # fieldnames = ["user_name", "status", "datetime"]
    # writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    # writer.writeheader()

#parse through senator data file to get twitter user id
with open("Democrats/data/dem_data/dem_ids.txt", "r") as data:
    for line in data:
        line = line.split()
        for word in line:
            try:
                int(word)
                dem_id_list.append(str(word))
            except ValueError:
                continue

while(1):
    try:
        print("connecting to Democate Stream...")
        myStream.filter(dem_id_list)
    except:
        pass

    logging.error(f"Democate Stream Failed {datetime.datetime.now()}")
    time.sleep(10)

