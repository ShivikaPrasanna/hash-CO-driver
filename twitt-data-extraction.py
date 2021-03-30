#Dev: Shivika
import json, sys
import argparse
from pathlib import Path
import datetime as DT

import tweepy
from tweepy import OAuthHandler
from tweepy.cursor import Cursor

ap = argparse.ArgumentParser()
ap.add_argument("-c", "--credentials", required=True,help="path to credentials file")
ap.add_argument("-o", "--output", required=True,help="path to dump tweets in json file")
args = vars(ap.parse_args())

credentials_path= str(args["credentials"])
output_file = str(args["output"])

if not output_file.lower().endswith('.json'):
    print("Output filename should contain .json extension.")

print("------------- RUNNING PARAMETERS ------------")
print("Credentials stored: " + credentials_path)
print("Output stored in JSON format: " + output_file)
#filepath = "../hash-CO-driver/twitter_credentials.json"

with open(credentials_path) as json_file:
    creds = json.load(json_file)
auth = tweepy.OAuthHandler(creds['CONSUMER_KEY'], creds['CONSUMER_SECRET'])
auth.set_access_token(creds['ACCESS_TOKEN'], creds['ACCESS_SECRET'])
api = tweepy.API(auth)

keyword = ("COVID-19 OR covid19 OR covid-19 OR coronavirus OR vaccination OR elections OR #COVID-19 OR #covid19 OR #covid-19 OR #coronavirus OR #vaccination OR #elections")
today = DT.date.today()
week_ago = today - DT.timedelta(days=7)

with open(output_file, 'w', encoding='utf8') as file:
    for tweet in tweepy.Cursor(api.search, q=keyword, lang='en', tweet_mode='extended',
    since=week_ago, wait_on_rate_limit=True).items(1000):
        json.dump(tweet._json, file, indent=2)

print(output_file, "size in bytes is: ", Path(output_file).stat().st_size)
