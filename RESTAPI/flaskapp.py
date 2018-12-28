from flask import Flask 
from flask import jsonify
import redis
import pysolr
import sys
from redis import ConnectionError
from datetime import datetime	
from app_props import *

app = Flask(__name__)

#Setup a redis connection
redisClient = redis.Redis(host=REDIS_ENDPOINT,port=REDIS_PORT, db=0)
try:
	#Test redis connection
	redisClient.ping()
except ConnectionError:
	sys.exit('Exiting !!! Not able to connect with Redis Cluster')

#Setup a solr connection
solr = pysolr.Solr('http://'+SOLR_ENDPOINT+':'+SOLR_PORT+'/solr/'+SOLR_CORE+'/', timeout=10)

@app.route('/top_hashtags')
def get_top_hashtags():
	"""Method to get top 10 trending tweets apart from fashion
	"""
	redis_hashtags_listname = REDIS_TRENDING_HASHTAGS_SET
	try:
		top_hashtags = redisClient.zrange(redis_hashtags_listname, 0, 10, withscores=True, desc=True)
	except:
		return jsonify({'status':500, 'Message':'Failed to complete your request'})
	return jsonify({'status':200, 'top_hashtags':top_hashtags})


@app.route('/tweets_count_per_minute')
def get_tweets_count_per_minute():
	"""Method to get the rate of tweets in past hour
	"""
	hour = int(datetime.utcnow().strftime('%H'))
	minute = int(datetime.utcnow().strftime('%M'))
	result={}
	try:
		for i in range(0,60):
			minute-=1
			if minute < 0:
				hour = hour-1 if hour>0 else 11
				minute = 59
			key = format(hour,'02d') + ":"+ format(minute,'02d')
			value = redisClient.get(key)
			result[key] = 0 if value==None else value
	except:
		return jsonify({'status':500, 'Message':'Failed to complete your request'})
	return jsonify({'status':200, 'utcnow': datetime.utcnow(),'tweets_rate':result})

@app.route('/show_tweets')
def show_latest_tweets():
	"""Method to get latest 100 tweets
	"""
	result=[]
	try:
		latest_tweets = solr.search(q='*:*', **{'fl':'tweet,created_at', 'fq':'created_at:[* TO NOW]', 'sort' : 'created_at desc', 'rows':100})
		for tweet in latest_tweets:
			result.append(str(tweet))		
	except:
		return jsonify({'status':500, 'Message':'Failed to complete your request'})
	return jsonify({'status':200, 'tweets':result})

if __name__ == '__main__':
	app.run(host='0.0.0.0')