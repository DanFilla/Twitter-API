
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

today = datetime.datetime.today()
today = today.strftime(today.strftime("%b-%d-%Y"))


# Tweet the plot.
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)

api = tweepy.API(auth)

# media = api.media_upload(f"{today}_hourplt.png")
# media = api.update_with_media(f"{today}_hourplt.png")



print(datetime.datetime.today().day)
