import tweepy
import threading
import logging
import datetime
import time
import csv
import os
from Democrats.DemStream.classes.StreamClass import MyStreamListener

logging.basicConfig(filename="logging-files/dem_logs.log")

consumer_key = os.environ["CONSUMER_KEY"]
consumer_secret = os.environ["CONSUMER_SECRET"]

key = os.environ["KEY"]
secret = os.environ["SECRET"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)

myStreamListener = MyStreamListener()

myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

dem_id_list = []

with open("Democrats/data/dem_data/dem_status_data.csv", newline='') as csv_file:
    rea = csv.reader(csv_file)
    has_header = False
    for x in rea:
        if x == ['user_name', 'status', 'datetime']:
            has_header = True
        break

if not has_header:
    with open("Democrats/data/dem_data/dem_status_data.csv", "w") as csv_file:
            fieldnames = ["user_name", "status", "datetime"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

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
        logging.error(f"Democate Stream Failed {datetime.datetime.now()}")
        time.sleep(10)


