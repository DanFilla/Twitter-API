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
    dem_df = pd.read_csv("../Democrats/data/dem_data/dem_status_data_former.csv")
    rep_df = pd.read_csv("../Republicans/data/rep_data/rep_status_data_former.csv")

    #day and hour tweet dataframe. key = day
    #                              value = array of the hours each tweet was tweeted.

    rep_date_list = {}

    for j in range(len(rep_df['datetime'])):
        day = datetime.datetime.strptime(rep_df['datetime'].iloc[j], "%Y-%m-%d %H:%M:%S.%f").day
        rep_date_list[day] = []

    for i in range(len(rep_df['datetime'])):
        day = datetime.datetime.strptime(rep_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").day
        hour = datetime.datetime.strptime(rep_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").hour
        rep_date_list[day] = rep_date_list.get(day) + [hour]

    dem_date_list = {}

    for j in range(len(dem_df['datetime'])):
        day = datetime.datetime.strptime(dem_df['datetime'].iloc[j], "%Y-%m-%d %H:%M:%S.%f").day
        dem_date_list[day] = []

    for i in range(len(dem_df['datetime'])):
        day = datetime.datetime.strptime(dem_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").day
        hour = datetime.datetime.strptime(dem_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").hour
        dem_date_list[day] = dem_date_list.get(day) + [hour]

    #Get week range.
    week_end = datetime.datetime.today()
    week_start = week_end - datetime.timedelta(days=7)
    week_range = range(week_start.day, week_end.day)

    rep_week_plot = []
    dem_week_plot = []
    for num in week_range:
        rep_week_plot.append(len(rep_date_list.get(num)))
        dem_week_plot.append(len(dem_date_list.get(num)))

    #save graph
    plt.plot(week_range, rep_week_plot, label="Republicans", color="r")
    plt.plot(week_range, dem_week_plot, label="Democrats", color="b")
    plt.legend(loc="upper left")
    plt.xlabel("Days")
    plt.ylabel("Number of Tweets")
    plt.savefig(f"{today}_weekplt.png", bbox_inches="tight")

    #tweet the graph
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)

    api = tweepy.API(auth)

    api.media_upload(f"{today}_weekplt.png")

print("Initalizing Schedule...")

schedule.every().day.at("23:00").do(day)
schedule.every().sunday.at("23:00").do(week)

while 1:
    schedule.run_pending()
    time.sleep(3600)

