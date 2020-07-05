#!/usr/bin/env python
# coding: utf-8
import tweepy

import sys
sys.path.append('/Users/dan/Desktop/Twitter-API/keys')
from secret_keys import *

import numpy as np
import pandas as pd
import datetime
# import nltk; nltk.download('popular')
from collections import defaultdict
import matplotlib.pyplot as plt
import schedule
import time
plt.close('all')

def day():
    dem_df = pd.read_csv("../Democrats/data/dem_data/dem_status_data.csv")
    rep_df = pd.read_csv("../Republicans/data/rep_data/rep_status_data.csv")

    #Democrate day and hour tweet dataframe. key = day value = hour.
    dem_date_list = {}

    for j in range(len(dem_df['datetime'])):
        day = datetime.datetime.strptime(dem_df['datetime'].iloc[j], "%Y-%m-%d %H:%M:%S.%f").day
        dem_date_list[day] = []

    for i in range(len(dem_df['datetime'])):
        day = datetime.datetime.strptime(dem_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").day
        hour = datetime.datetime.strptime(dem_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").hour
        dem_date_list[day] = dem_date_list.get(day) + [hour]

    #Republican day and hour tweet dataframe. key = day
    #                                         value = array of the hours each tweet was tweeted.
    rep_date_list = {}

    for j in range(len(rep_df['datetime'])):
        day = datetime.datetime.strptime(rep_df['datetime'].iloc[j], "%Y-%m-%d %H:%M:%S.%f").day
        rep_date_list[day] = []

    for i in range(len(rep_df['datetime'])):
        day = datetime.datetime.strptime(rep_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").day
        hour = datetime.datetime.strptime(rep_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").hour
        rep_date_list[day] = rep_date_list.get(day) + [hour]

    hour_range = range(0, 24)

    current_day = datetime.datetime.today().day

    rep_temp = set(rep_date_list.get(current_day))
    dem_temp = set(dem_date_list.get(current_day))

    rep_tweet_count = []
    dem_tweet_count = []

    for num in hour_range:
        if num not in rep_temp:
            rep_tweet_count.append(0)
        else:
            rep_tweet_count.append(rep_date_list.get(current_day).count(num))

        if num not in dem_temp:
            dem_tweet_count.append(0)
        else:
            dem_tweet_count.append(dem_date_list.get(current_day).count(num))

    #Save the plot
    plt.plot(hour_range, rep_tweet_count, label="Republican", color="r")
    plt.plot(hour_range, dem_tweet_count, label="Democrats", color="b")
    plt.legend(loc="upper left")
    plt.xlabel("Hours")
    plt.ylabel("Number of Tweets")

    today = datetime.datetime.today()
    today = today.strftime(today.strftime("%b-%d-%Y"))

    plt.savefig(f"{today}_hourplt.png", bbox_inches="tight")

    # Tweet the plot.
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)

    api = tweepy.API(auth)

    api.media_upload(f"{today}_hourplt.png")

def week():
    pass




print("Initalizing Schedule...")

schedule.every().day.at("23:00").do(day)

while 1:
    schedule.run_pending()
    time.sleep(3600)

