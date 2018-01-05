import tweepy
import datetime
import sys
import os

# User defined variables
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""
username = "realdonaldtrump"
get_old_tweets_path = "/home/ubuntu/GetOldTweets-python"

# Logs a message to the daily log file
def log(log_file_path, message):
    if os.path.exists(log_file_path):
        log_file = open(log_file_path, "r")
        write_buffer = log_file.read()
        log_file.close()
    else:
        write_buffer = ""
    log_file = open(log_file_path, "w")
    timestamp = str(datetime.datetime.now())
    write_buffer += "%s -- %s\n" % (timestamp, message)
    log_file.write(write_buffer)
    log_file.close()

# Set up authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Authenticate and create the API object
api = tweepy.API(auth)

# Set up the date to search for tweets
now = datetime.datetime.now()
year = now.year - 4
month = now.month
day = now.day

# Set up the path for the log file
log_file_path = "logs/%s-%s-%s.log" % (year, month, day)

# Check if the tweets have already been downloaded
csv_file = "downloaded_tweets/%s-%s-%s.csv" % (year, month, day)
downloaded = os.path.exists(csv_file)

# Download tweets if necessary
if not downloaded:
    sys.path.append(get_old_tweets_path)
    import Exporter
    since_date = "%s-%s-%s" % (year, month, day)
    until_date = "%s-%s-%s" % (year, month, day+1)
    args = ["--username", username, "--since", since_date, "--until", until_date, csv_file]
    Exporter.main(args)
    os.rename("output_got.csv", csv_file)

# Get the list of tweets which have already been retweeted
retweeted_filepath = "retweeted_ids/%s-%s-%s.csv" % (year, month, day)
retweeted_ids = []
if os.path.exists(retweeted_filepath):
    retweeted_file = open(retweeted_filepath, "r")
    retweeted_id_strings = retweeted_file.readlines()
    for id_string in retweeted_id_strings:
        retweeted_ids.append(int(id_string))
    retweeted_file.close()

# Parse the downloaded tweets
raw_tweet_data = open(csv_file).readlines()
tweet_data = []
for line in raw_tweet_data:
    tweet_data.append(line.split(";"))
tweet_data = tweet_data[1:]
tweet_data.reverse()

# Retweet tweets which occurred before the current time
for tweet in tweet_data:
    id = int(tweet[8].replace('"', ""))
    text = tweet[4]
    time = tweet[1].split(" ")[1].split(":")
    tweet_hour = int(time[0])
    tweet_minute = int(time[1])
    current_hour = int(now.hour)
    current_minute = int(now.minute)
    if tweet_hour < current_hour or (tweet_hour == current_hour and tweet_minute <= current_minute):
        if text[1] != "@":
            if not id in retweeted_ids:
                try: 
                    api.retweet(id)
                    message = "Retweeted tweet id: " + str(id)
                    print message
                    log(log_file_path, message)
                except: 
                    message = "Unable to retweet id: " + str(id)
                    print message
                    log(log_file_path, message)
                finally:
                    retweeted_ids.append(id)

# Save the list of retweeted ids
if len(retweeted_ids) > 0:
    write_buffer = ""
    retweeted_file = open(retweeted_filepath, "w")
    for id in retweeted_ids:
        write_buffer += str(id) + "\n"
    write_buffer = write_buffer[:-1]
    retweeted_file.write(write_buffer)
    retweeted_file.close()

