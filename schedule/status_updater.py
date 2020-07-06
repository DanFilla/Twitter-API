#!/usr/bin/env python
# coding: utf-8
import tweepy

import matplotlib

import os
import numpy as np
import pandas as pd
import datetime
import nltk; nltk.download('popular')
from collections import defaultdict
import matplotlib.pyplot as plt
import schedule
import time
plt.close('all')
matplotlib.use('Agg')

consumer_key = os.environ["CONSUMER_KEY"]
consumer_secret = os.environ["CONSUMER_SECRET"]

key = os.environ["KEY"]
secret = os.environ["SECRET"]

def trending_words(rep, dem):
    status_list_rep = []
    status_list_dem = []
    status_dict = {}

    for status in rep['status']:
        for word in status.split():
            token = nltk.word_tokenize(word)
            tagged = nltk.pos_tag(token)
            if tagged[0][1][0] == 'N' and word[0] != "@" and word[:4].lower() != "http":
                status_list_rep.append(word.lower())

    for status in dem['status']:
        for word in status.split():
            token = nltk.word_tokenize(word)
            tagged = nltk.pos_tag(token)
            if tagged[0][1][0] == 'N' and word[0] != "@" and word[:4].lower() != "http":
                status_list_dem.append(word.lower())

    word_dict_rep = {}
    word_dict_dem = {}

    for word in status_list_rep:
        if word not in word_dict_rep.keys():
            word_dict_rep[word] = 0
        else:
            word_dict_rep[word] = word_dict_rep.get(word) + 1

    for word in status_list_dem:
        if word not in word_dict_dem.keys():
            word_dict_dem[word] = 0
        else:
            word_dict_dem[word] = word_dict_dem.get(word) + 1

    word_dict_rep = sorted(word_dict_rep.items(), key=lambda x: x[1], reverse=True)
    word_dict_dem = sorted(word_dict_dem.items(), key=lambda x: x[1], reverse=True)

    tweet = "Republicans:\n"
    for tup in word_dict_rep[:10]:
        tweet += "\t" + str(tup[0]) + " => " + str(tup[1]) + "\n"

    tweet += "\nDemocrats:\n"
    for tup in word_dict_dem[:10]:
        tweet += "\t" + str(tup[0]) + " => " + str(tup[1]) + "\n"

    return tweet



def day():
    dem_df = pd.read_csv("Democrats/data/dem_data/dem_status_data.csv")
    rep_df = pd.read_csv("Republicans/data/rep_data/rep_status_data.csv")

    current_day = datetime.datetime.today().day
    hour_range = range(0, 24)

    #Democrate day and hour tweet dataframe. key = day value = hour.

    dem_date_list = {}

    for j in range(len(dem_df['datetime'])-1, 0, -1):
        day = datetime.datetime.strptime(dem_df['datetime'].iloc[j], "%Y-%m-%d %H:%M:%S.%f").day
        if day == current_day-1:
            break
        dem_date_list[day] = []

    for i in range(len(dem_df['datetime'])-1, 0, -1):
        day = datetime.datetime.strptime(dem_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").day
        hour = datetime.datetime.strptime(dem_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").hour
        if day == current_day-1:
            break
        dem_date_list[day] = dem_date_list.get(day) + [hour]

    #Republican day and hour tweet dataframe. key = day
    #                                         value = array of the hours each tweet was tweeted.
    rep_date_list = {}

    for j in range(len(rep_df['datetime'])-1, 0, -1):
        day = datetime.datetime.strptime(rep_df['datetime'].iloc[j], "%Y-%m-%d %H:%M:%S.%f").day
        if day == current_day-1:
            break
        rep_date_list[day] = []

    for i in range(len(rep_df['datetime'])-1, 0, -1):
        day = datetime.datetime.strptime(rep_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").day
        hour = datetime.datetime.strptime(rep_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").hour
        if day == current_day-1:
            break
        rep_date_list[day] = rep_date_list.get(day) + [hour]



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

    plt.savefig(f"Schedule/{today}_hourplt.png", bbox_inches="tight")

    # Tweet the plot.
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(key, secret)

    api = tweepy.API(auth)

    api.update_with_media(f"{today}_hourplt.png", status=trending_words(rep_df, dem_df))
    # api.update_with_media(f"Schedule/{today}_hourplt.png")

def week():
    dem_df = pd.read_csv("Democrats/data/dem_data/dem_status_data.csv")
    rep_df = pd.read_csv("Republicans/data/rep_data/rep_status_data.csv")

    #Get week range.
    week_end = datetime.datetime.today()
    week_start = week_end - datetime.timedelta(days=7)
    week_range = range(week_start.day, week_end.day)

    #Republican day and hour tweet dataframe. key = day
#                                             value = array of the hours each tweet was tweeted.


    #collecting tweet data for Republicans
    rep_date_list = {}
    for j in range(len(rep_df['datetime'])-1, 0, -1):
        day = datetime.datetime.strptime(rep_df['datetime'].iloc[j], "%Y-%m-%d %H:%M:%S.%f").day
        if day == week_start.day-1:
            break
        rep_date_list[day] = []

    for i in range(len(rep_df['datetime'])-1, 0, -1):
        day = datetime.datetime.strptime(rep_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").day
        hour = datetime.datetime.strptime(rep_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").hour
        if day == week_start.day-1:
            break
        rep_date_list[day] = rep_date_list.get(day) + [hour]

    #Collecting tweet data for Democrats
    dem_date_list = {}
    for j in range(len(dem_df['datetime'])-1, 0, -1):
        day = datetime.datetime.strptime(dem_df['datetime'].iloc[j], "%Y-%m-%d %H:%M:%S.%f").day
        if day == week_start.day-1:
            break
        dem_date_list[day] = []

    for i in range(len(dem_df['datetime'])-1, 0, -1):
        day = datetime.datetime.strptime(dem_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").day
        hour = datetime.datetime.strptime(dem_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").hour
        if day == week_start.day-1:
            break
        dem_date_list[day] = dem_date_list.get(day) + [hour]

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

    api.media_upload(f"{today}_weekplt.png", status=trending_words(rep_df, dem_df))

print("Initalizing Schedule...")

schedule.every().day.at("23:00").do(day)
schedule.every().sunday.at("23:00").do(week)

while 1:
    print("Sleeping!!!")
    schedule.run_pending()
    time.sleep(3600)
