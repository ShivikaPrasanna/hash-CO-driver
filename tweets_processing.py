#Dev: Shivika
import json, sys, os
import argparse
from pathlib import Path
import pandas as pd
import csv
import re

import tweepy
from tweepy import OAuthHandler

ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True, help="directory containing all .json files")
args = vars(ap.parse_args())

directory = str(args["directory"])

print("------------- RUNNING PARAMETERS ------------")
print("JSON files stored in: " + directory + "\n")

all_files = []
skip = ['twitter_credentials.json', 'projdata_Mar11.json', 'projdata_Mar30.json', 'projdata_Mar30_AG.json', 'projdata_Mar13.json', 'projdata_Mar23.json']
for all_files in os.listdir(directory):
    if all_files.endswith('.json') and all_files not in skip:
        path = os.path.join(directory, all_files)
        print("JSON file being processed: ", path)

counter = 0
tot_tweets = 0
data = []
hashtag_list = set()
dictionary = {}

# punctuation = '!"$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
# def clean_tweets(tweet):
#     tweet = "".join([word.lower() for word in tweet if word not in punctuation]) # remove puntuation
#     tweet = re.sub('[0-9]+', '', tweet)
#     tweet = re.sub("@\S+", " ", tweet)
#     tweet = re.sub("https*\S+", " ", tweet)
#     # tweet = re.sub("#\S+", " ", tweet)
#     tweet = tweet.encode('ascii', 'ignore').decode()
#
#     return tweet

for file in [f for f in os.listdir(directory) if f.endswith('.json') and f not in skip]:
    path = os.path.join(directory, file)
    with open(path) as json_file:
        print(path)
        s = json_file.read()
        s = s.replace('\t','')
        s = s.replace('\n','')
        s = s.replace('}{','},{')
        s = s.replace('} {','},{')
        data = json.loads("[{}]".format(s))

        # for line in data:
        #     data.append(json.loads(s))
        for item in data:
            tot_tweets += 1
            if 'id_str' in item:
                key = item['id_str']
                # if key in check:
                #     print(key, item)
                if 'full_text' in item:
                    val = item['full_text']
                # val = clean_tweets(val)
                if val not in dictionary:
                    counter += 1
                    if counter % 100 == 0:
                        print("Check: ", counter)
                    dictionary[val] = key
            if 'entities' in item:
                for hashtag in item['entities']['hashtags']:
                    hashtag_list.add(hashtag['text'])

print("Total number of tweets: ", tot_tweets, "\n")
print("Number of unique tweets: ", len(dictionary), "\n")
print("Number of unique hashtags: ", len(hashtag_list), "\n")
print("List of hashtags: ", hashtag_list, "\n")
