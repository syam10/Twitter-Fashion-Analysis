## KafkaToSolr
Tweets are consumed from Kafka, transform the tweet json and store it in Apache Solr

### Key Points
1. While transforming the tweet json, we collect all the hashtags in tweet except #fashion and store it in Redis sorted set data structure so that we can retrieve all the trending hashhtags. If hashtag is new, we create a new key in redis or else we increment existing key.

2. Transforming the tweet json we store only few necessary attributes in solr(like created_at, user_id, tweet_id, tweet_text)