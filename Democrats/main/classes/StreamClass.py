import tweepy
import datetime

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

        if (from_creator(status)):

            tweet_data = open("../data/dem_data/dem_status_data.txt", "a")

            print("Some douche-bag tweeted!!!")

            print(status._json['user']['name'])


            tweet_data.write("\n")
            tweet_data.write("****************************")
            tweet_data.write("\n")
            if hasattr(status, "retweeted_status"):
                try:
                    tweet_data.write(status.retweeted_status.extended_tweet["full_text"])
                except AttributeError:
                    tweet_data.write(status.retweeted_status.text)

            else:
                try:
                    tweet_data.write(status.extended_tweet["full_text"])
                except AttributeError:
                    tweet_data.write(status.text)
            tweet_data.write("\n")
            tweet_data.write("****************************")
            tweet_data.write("\n")
            tweet_data.close()
        else:
            print(f"ignored status {datetime.datetime.now()}")
