## KafkaToSolr
Tweets are generated from Twitter Streaming API and publish it in kafka topic

### Key Points
1. After generating the tweets from API, to find the tweet rate we create a key with UTC Timezone %H:%M format and create/update the value of it with the count of tweets obtained in that minute.
2. As keys in redis will be increasing for every hour we should have a cron job to delete the old keys which are created prior to an hour from current time