#!/usr/bin/env python
# coding: utf-8

# In[49]:

import tweepy

import sys
sys.path.append('/Users/dan/Desktop/Twitter-API/keys')
from secret_keys import *

import numpy as np
import pandas as pd
import datetime
import nltk; nltk.download('popular')
from collections import defaultdict
import matplotlib.pyplot as plt
import schedule
import time
plt.close('all')

# def job():
    # dem_df = pd.read_csv("../Democrats/data/dem_data/dem_status_data.csv")
    # rep_df = pd.read_csv("../Republicans/data/rep_data/rep_status_data.csv")

    # rep_date_list = []
    # for i in range(len(rep_df['datetime'])):
        # rep_date_list.append(datetime.datetime.strptime(rep_df['datetime'].iloc[i], "%Y-%m-%d %H:%M:%S.%f").hour)

    # dem_date_list = []
    # for j in range(len(dem_df['datetime'])):
        # dem_date_list.append(datetime.datetime.strptime(dem_df['datetime'].iloc[j], "%Y-%m-%d %H:%M:%S.%f").hour)


    # current_date = datetime.datetime.now().strftime('%m-%d-%y')

    # #needs to be 24 hours.
    # date_range = pd.date_range(start='06-12-2020', end=current_date, freq='1H').day
    # print(date_range)

    # # Find out how many tweets were tweeted on each day
    # # For the Republicans
    # temp = set(rep_date_list)
    # rep_freq_list = []

    # for x in temp:
        # rep_freq_list.append(rep_date_list.count(x))

    # temp = list(temp)
    # print(rep_freq_list)

    # # Find out how many tweets were tweeted on each day
    # # For the Democrats
    # temp = set(dem_date_list)
    # dem_freq_list = []

    # for x in temp:
        # dem_freq_list.append(dem_date_list.count(x))

    # temp = list(temp)

    # print(dem_freq_list)

    # plt.plot(date_range, rep_freq_list, label="Republican", color='r')
    # plt.plot(date_range, dem_freq_list, label="Democrat", color='b')
    # plt.legend(loc="upper left")
    # plt.xlabel("Dates")
    # plt.ylabel("Number of Tweets")
    # # plt.show()


    # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(key, secret)

    # api = tweepy.API(auth)

    # api.media_upload(plt.show())


def job():
    dem_df = pd.read_csv("../Democrats/data/dem_data/dem_status_data_former.csv")
    rep_df = pd.read_csv("../Republicans/data/rep_data/rep_status_data_former.csv")

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
            rep_tweet_count.append(rep_date_list.get(18).count(num))

        if num not in dem_temp:
            dem_tweet_count.append(0)
        else:
            dem_tweet_count.append(dem_date_list.get(18).count(num))

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

schedule.every().day.at("23:00").do(job)
# schedule.every(1).minutes.do(job)

while 1:
    schedule.run_pending()
    time.sleep(3600)

# parse user names out of the dataframe

# dem_name_list = []
# rep_name_list = []

# for name in dem_df['user_name']:
    # dem_name_list.append(str(name))

# for name in rep_df['user_name']:
    # rep_name_list.append(str(name))


# # In[60]:


# dem_names = set(dem_df['user_name'])
# rep_names = set(rep_df['user_name'])


# all_name_count = {}

# for name in dem_names:
    # all_name_count[name] = dem_name_list.count(name)

# for name in rep_names:
    # all_name_count[name] = rep_name_list.count(name)


# all_name_count = sorted(all_name_count.items(), key=lambda x: x[1], reverse=True)


# # In[61]:


# fig = plt.figure(figsize=(15,5))

# for x in all_name_count:
    # if x[0] in dem_name_list:
        # plt.bar(x[0], x[1], color=('b'))
    # elif x[0] in rep_name_list:
        # plt.bar(x[0], x[1], color=('r'))


# plt.xticks(rotation='vertical', fontsize=10)
# plt.ylabel("Number of Tweets")
# plt.show()


# # In[62]:


# fig = plt.figure(figsize=(5,5))

# for x in all_name_count[:10]:
    # if x[0] in dem_name_list:
        # plt.bar(x[0], x[1], color=('b'))
    # elif x[0] in rep_name_list:
        # plt.bar(x[0], x[1], color=('r'))


# plt.xticks(rotation='vertical')
# plt.ylabel("Number of Tweets")
# plt.show()


# # In[63]:


# # Get statuses from dataframe in string form.

# status_list = []
# status_dict = {}

# for status in dem_df['status']:
    # for word in status.split():
        # token = nltk.word_tokenize(word)
        # tagged = nltk.pos_tag(token)
        # if tagged[0][1][0] == 'N':
            # status_list.append(word.lower())


# set_status_list = set(status_list)

# for word in set_status_list:
    # status_dict[word] = status_list.count(word)

# status_dict = sorted(status_dict.items(), key=lambda x: x[1], reverse=True)
# table_list = []

# for tup in status_dict[:10]:
    # tup = list(tup)
    # tup[1] = str(tup[1])
    # table_list.append(tup)

# plt.table(table_list, loc='top')
# plt.show()


# # In[64]:


# status_list = []
# status_dict = {}

# for status in rep_df['status']:
    # for word in status.split():
        # token = nltk.word_tokenize(word)
        # tagged = nltk.pos_tag(token)
        # if tagged[0][1][0] == 'N':
            # status_list.append(word.lower())


# set_status_list = set(status_list)

# for word in set_status_list:
    # status_dict[word] = status_list.count(word)

# status_dict = sorted(status_dict.items(), key=lambda x: x[1], reverse=True)

# for tup in status_dict[:10]:
    # print(tup)


# # In[ ]:





# # schedule.every(10).seconds.do(job)

# # while 1:
    # # schedule.run_pending()
    # # time.sleep(1)

