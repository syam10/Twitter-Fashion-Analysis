# Twitter-Fashion-Analysis
Real time #fashion analysis use case that streams tweets in Kafka and persists it in Apache Solr. API's in Flask to access data.

![alt text](https://github.com/syam10/Twitter-Fashion-Analysis/blob/master/flow_diagram.png)


### Prerequisites

1. To run the application, you need the following clusters to be installed and running
```
Kafka
Apache Solr
Redis
```

2. Once the above mentioned clusters are up and running, update app_props file in each module which are cluster related parameters used in application

3. Make sure you install following python libraries in the server
```
pip install tweepy --user
pip install kafka-python --user
pip install redis --user
pip install Flask --user
```

### Running Application

1. Login into server and execute flaskapp.py in RESTAPI module to start flask application
```
python RESTAPI/flaskapp.py
```
2. Execute twitter_consumer.py in TwitterToKafka module to get tweets from twitter and stream it in kafka
```
python TwitterToKafka/twitter_consumer.py
```
3. Execute persist_tweets.py in KafkaToSolr module to store tweets in solr
```
python KafkaToSolr/persist_tweets.py
```
