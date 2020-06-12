import tweepy
import datetime
import csv

def from_creator(status):
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        fieldnames = ["user_name", "status", "datetime"]
        opened_file = open("../data/dem_data/dem_status_data.csv", "a")
        tweet_data = csv.DictWriter(opened_file, fieldnames=fieldnames)

        user_name = status._json['user']['name']
        date_time = datetime.datetime.now()

        if (from_creator(status)):

            print("Some douche-bag tweeted!!!")
            print(user_name)

            if hasattr(status, "retweeted_status"):
                try:
                    extended_user_status = status.retweeted_status.extended_tweet["full_text"]
                    tweet_data.writerow({"user_name": user_name, 'status': extended_user_status, 'datetime': date_time})
                except AttributeError:
                    user_status = status.retweeted_status.text
                    tweet_data.writerow({"user_name": user_name, 'status': user_status, 'datetime': date_time})

            else:
                try:
                    extended_user_status = status.extended_tweet["full_text"]
                    tweet_data.writerow({"user_name": user_name, 'status': extended_user_status, 'datetime': date_time})
                except AttributeError:
                    user_status = status.text
                    tweet_data.writerow({"user_name": user_name, 'status': user_status, 'datetime': date_time})
        else:
            print(f"ignored status {datetime.datetime.now()}")
