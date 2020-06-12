import tweepy
import threading
import logging
import datetime
import time
import os
import csv
from classes.StreamClass import MyStreamListener

logging.basicConfig(filename='../../logging-files/rep_logs.log')

consumer_key = "O440GKDKaFDlouDj5nutK0d6N"
consumer_secret = "byeBjTsocrXgNoBW8XMv4p1jUGVU6SUTMv1UhzQAfaSLFYV1a4"

key = "1083113049568038924-lMexUYQA0r06vwunKoSwhufa9QG4Es"
secret = "jIT1NclZ4zd8nY5IA2hc7MabBPrussrECVDMtZrtBYcaW"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)

myStreamListener = MyStreamListener()

myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

rep_id_list = []

with open("../data/rep_data/rep_status_data.csv", "a") as csv_file:
    if os.stat("../data/rep_data/rep_status_data.csv") == 0:
        fieldnames = ["user_name", "status", "datetime"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
    else:
        pass

#parse through senator data file to get twitter user id
with open("../data/rep_data/rep_ids.txt", "r") as data:
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
        print("connecting...")
        myStream.filter(rep_id_list)
    except:
        pass

    print("trying...")
    logging.error(f"Republican Stream Failed {datetime.datetime.now()}")
    time.sleep(10)
