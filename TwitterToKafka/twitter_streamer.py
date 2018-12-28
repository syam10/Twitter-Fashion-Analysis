from app_props import *
from tweets_output_consumer import TweetsOutputConsumer
from tweepy import OAuthHandler
from tweepy import Stream

class TwitterStreamer(object):
	"""
	Class for Streaming real time tweets from Twitter
	"""
	def __init__(self):
		pass

	def stream_tweets(self, hash_tag_list, kafka_producer, redis_client):
                # Handles Twitter authetification and the connection to Twitter Streaming API
                listener = TweetsOutputConsumer(kafka_producer, redis_client)
                auth = OAuthHandler(TWITTER_CREDS_CONSUMER_KEY, TWITTER_CREDS_SECRET_KEY)
                auth.set_access_token(TWITTER_CREDS_ACCESS_TOKEN, TWITTER_CREDS_ACCESS_TOKEN_SECRET)
                stream = Stream(auth, listener)

                #Filter Twitter Streams to capture data by the keywords	
                stream.filter(track=hash_tag_list)	
