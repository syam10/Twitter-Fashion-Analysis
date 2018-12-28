import json
from datetime import datetime
import dateutil.parser


class TweetParser(object):
	"""Class to parse the tweet obtained from twitter streaming api
	"""
	def __init__(self):
		pass

	def getTweetText(self, tweet):
		return tweet['text']

	def getTweetHashtags(self, tweet):
		hashtagsObject = tweet['entities']['hashtags']
		hashtagsList = []
		for i in range(0, len(hashtagsObject)):
			hashtagsList.append(hashtagsObject[i]['text'])
		return hashtagsList

	def getDatetimeFormat(self, tweet):
		timestamp = datetime.strptime(tweet['created_at'],
                   '%a %b %d %H:%M:%S +0000 %Y')
		timestamp_string =  datetime.strftime(timestamp, '%Y-%m-%dT%H:%M:%S%Z') 
		timestamp_obj = dateutil.parser.parse(timestamp_string)
		return timestamp_obj

	def getTweetId(self, tweet):
		return tweet['id']

	def getUserId(self, tweet):
		return tweet['user']['id']

