import argparse
import tweepy
import configparser
import label
from tweepy import OAuthHandler
import wget
import os
from urllib.parse import urlparse

def main(url):
    #Parse the url and get the username
    userName = urlparse(url)[2][1:]
    #Locate the config file and connect API
    config = parse_config('./resources/config.cfg')
    auth = authorise_twitter_api(config)
    api = tweepy.API(auth)

    #5th argument is the number of medias to download
    download_images(api, userName, False, False, 1, './resources/images/'+userName+"/")

def download_images(api, username, retweets, replies, num_tweets, output_folder):
    tweets = api.user_timeline(screen_name=username, count=200, include_rts=retweets, exclude_replies=replies)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    downloaded = 0
    while (len(tweets) != 0):
        last_id = tweets[-1].id

        for status in tweets:
            #Add media filter to only receive images.
            media = status.entities.get('media', [])
            if (len(media) > 0 and downloaded < num_tweets):
                image = wget.download(media[0]['media_url'], out=output_folder)
                downloaded += 1
                #Call Google Vision API with the downloaded image
                label.main(image)

        tweets = api.user_timeline(screen_name=username, count=200, include_rts=retweets, exclude_replies=replies,
                                   max_id=last_id - 1)


def parse_config(config_file):
  config = configparser.ConfigParser()
  config.read(config_file)
  return config

def authorise_twitter_api(config):
  auth = OAuthHandler(config['DEFAULT']['consumer_key'], config['DEFAULT']['consumer_secret'])
  auth.set_access_token(config['DEFAULT']['access_token'], config['DEFAULT']['access_secret'])
  return auth

# [START run_application]
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('profile')
    args = parser.parse_args()
    main(args.profile)
    #photos.main()
# [END run_application]ben