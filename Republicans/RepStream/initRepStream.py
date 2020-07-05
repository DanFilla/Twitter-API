import sys
sys.path.append('/Users/dan/Desktop/Twitter-API/keys')
import tweepy
import threading
import logging
import datetime
import time
import os
import csv
from secret_keys import *
from Republicans.RepStream.classes.StreamClass import MyStreamListener

logging.basicConfig(filename='logging-files/rep_logs.log')

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)

myStreamListener = MyStreamListener()

myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

rep_id_list = []

# with open("Republican/data/rep_data/rep_status_data.csv", "a") as csv_file:
    # if os.stat("Republican/data/rep_data/rep_status_data.csv") == 0:
        # fieldnames = ["user_name", "status", "datetime"]
        # writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        # writer.writeheader()
    # else:
        # pass

#parse through senator data file to get twitter user id
with open("Republicans/data/rep_data/rep_ids.txt", "r") as data:
    for line in data:
        line = line.split()
        for word in line:
            try:
                int(word)
                rep_id_list.append(str(word))
            except ValueError:
                continue

while(1):
    try:
        print("connecting to Republican stream...")
        myStream.filter(rep_id_list)
    except:
        logging.error(f"Republican Stream Failed {datetime.datetime.now()}")
        time.sleep(10)

