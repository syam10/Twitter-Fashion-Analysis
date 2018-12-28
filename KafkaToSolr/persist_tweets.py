import json
from datetime import datetime
import pysolr
import sys
from tweet_parser import TweetParser
from kafka import KafkaConsumer
import redis

from app_props import *

#Setup a solr connection
solr = pysolr.Solr('http://'+SOLR_ENDPOINT+':'+SOLR_PORT+'/solr/'+SOLR_CORE+'/', timeout=10)

# Create a redis client
redisClient = redis.Redis(host=REDIS_ENDPOINT,port=REDIS_PORT, db=0)

#Create a TweetParser instance to parse and transform tweets consumed from kafka
tweetParser = TweetParser()

#Form a kafka client Object
kafkaClient = KafkaConsumer(KAFKA_TOPIC,
                         group_id='my-group',
                         bootstrap_servers=KAFKA_BROKERS)

#Sorted set name in redis cluster
hashtags_list = REDIS_TRENDING_HASHTAGS_SET


def persist_doc_solr(tweet):
	"""Method to store a document in Solr
	"""
	tweet_obj = json.loads(tweet, strict=False)	
	#Form doc
	doc = {
			"user_id":tweetParser.getUserId(tweet_obj),
			"tweet" : tweetParser.getTweetText(tweet_obj),
			"hashtags" : tweetParser.getTweetHashtags(tweet_obj),
			"created_at" : tweetParser.getDatetimeFormat(tweet_obj)

	}

	#Update hashtags count in Redis
	for tag in doc["hashtags"]:
		if (tag.lower()!="fashion"):
			redisClient.zincrby(hashtags_list, 1, tag)
	
	#Add doc to Solr
	solr.add([doc])
	print("Successfully added a doc to solr")


if __name__ == '__main__':

	for message in kafkaClient:
		persist_doc_solr(message.value)
