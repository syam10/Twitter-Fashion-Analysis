from app_props import *
from twitter_streamer import TwitterStreamer
from kafka import KafkaProducer
import redis

if __name__ == '__main__':
	'''Main function to start the application i.e to consume real time tweets from twitter
	'''
	#hash tags list that you want to filter from twitter streaming api 
	hash_tag_list = ["#fashion"]

	#Setup kafka producer client
	kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_BROKERS)

	#setup redis client
	redis_client = redis.Redis(host=REDIS_ENDPOINT,port=REDIS_PORT, db=0)

	#Streaming real time tweets from Twitter Streaming API
	twitter_streamer = TwitterStreamer()
	twitter_streamer.stream_tweets(hash_tag_list, kafka_producer, redis_client)
