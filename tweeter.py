import pymysql

import re
import tweepy
# import nltk
from tweepy import OAuthHandler
from textblob import TextBlob

connection = pymysql.connect(host="localhost", user="root", password="", database="mydb1")
cursor = connection.cursor()


class TwitterClient:
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = '5L4iF101tBHb0vVUQ7uCph3LR'
        consumer_secret = 'kKCDjgvrIO012yCAE8FCsL6kcHDo344i0SJjSlm4FG2YxL7x5f'
        access_token = '2842121736-dv73nAcb76ssBtHt0YSimalWRnvOiwnyXeEE9SW'
        access_token_secret = 'MgeXZivCLXglBxxAjtPafsveVMQiJLeSTn82zCKm3JnpB'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=100000):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text

                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

    def main(self, username):
        # creating object of TwitterClient Class
        # inp = input("You: ")
        api = TwitterClient()

        # calling function to get tweets
        query = username

        tweets = api.get_tweets(query, count=200)

        # cursor.execute("insert into testtable2(id) values('"+tweet+"')")

        # picking positive tweets from tweets
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        # percentage of positive tweets
        positive = (format(100 * len(ptweets) / len(tweets)))
        print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
        # picking negative tweets from tweets
        ntweets = [t for t in tweets if t['sentiment'] == 'negative']
        # percentage of negative tweets
        negative = (format(100 * len(ntweets) / len(tweets)))
        print("negative tweets percentage:", negative)
        # percentage of neutral tweets
        neutral = (format(100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)))
        print("Neutral tweets percentage: {} %".format(100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)))



        # printing first 5 positive tweets
        print("\n\n tweets:")

        for tweet2 in ptweets[:100]:
            print(query)
            print(tweet2['text'])
            positivedata=(tweet2['text'])
          
            sql = "INSERT INTO tablename1 (name,positive) VALUES (%s,%s)"
            val = (query,positivedata )
            cursor.execute(sql, val)

            connection.commit()

            #sql = "INSERT INTO testtable2 (Id, Name) VALUES (%s,%s )"
            #print(sql)
            #val = (tweet2['text'], query)

            #cursor.execute(sql, val)
            # cursor.execute("insert into testtable2(id) values('"+tweet+"')")

            # print(tweet['text'])

        # printing first 5 negative tweets

        # if query== query:

        # sql = "DELETE  FROM testtable WHERE Name = '"+query+"'"
        # print(sql)

        if query == query:

            for tweet3 in ntweets[:100]:
                print(query)
                print(negative)
                print(tweet3['text'])
                print(tweet2['text'])


                sql = "INSERT INTO tweeterdata ( negative,twwetname,nsrate,psrate,neutral) VALUES (%s,%s,%s,%s ,%s)"
                val = ( tweet3['text'], query, negative,positive,neutral)
                cursor.execute(sql, val)

                connection.commit()

                #sql = "INSERT INTO testtable (tweets, Name,negative) VALUES (%s,%s,%s )"
                #val = (tweet['text'], query, negative)

                #cursor.execute(sql, val)
                # cursor.execute("insert into testtable2(id) values('"+tweet+"')")

                # print(tweet['text'])
                #
                # cursor.execute("insert into testtable2 (id) VALUES (%s)",(tweets['text']))
                # cursor.execute("insert into testtable2(id) values('"+tweet+"')")


def main(inp):
    # creating object of TwitterClient Class
    #inp = input("You: ")
    api = TwitterClient()

    # calling function to get tweets
    query = inp

    tweets = api.get_tweets(query, count=200)

    # cursor.execute("insert into testtable2(id) values('"+tweet+"')")

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(tweets)))
    # picking negative tweets from tweets
    ntweets = [t for t in tweets if t['sentiment'] == 'negative']
    # percentage of negative tweets
    negative = (format(100 * len(ntweets) / len(tweets)))
    print("negative tweets percentage:", negative)
    # percentage of neutral tweets
    print("Neutral tweets percentage: {} %".format(100 * (len(tweets) - len(ntweets) - len(ptweets)) / len(tweets)))
    labels = 'Python', 'C++', 'Ruby', 'Java'
    sizes = ['negative', 130, 245, 210]
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    explode = (0.1, 0, 0, 0)  # explode 1st slice

    # Plot

    # printing first 5 positive tweets
    print("\n\n tweets:")

    for tweet2 in ptweets[:100]:
        print(query)
        print(tweet2['text'])
       # sql = "INSERT INTO testtable2 (Id, Name) VALUES (%s,%s )"
       # print(sql)
       # val = (tweet1['text'], query)

        #cursor.execute(sql, val)
        # cursor.execute("insert into testtable2(id) values('"+tweet+"')")

        # print(tweet['text'])

    # printing first 5 negative tweets

    # if query== query:

    # sql = "DELETE  FROM testtable WHERE Name = '"+query+"'"
    # print(sql)

    if query == query:

        for tweet in ntweets[:100]:
            print(query)
            print(negative)
            print(tweet['text'])






            # cursor.execute("insert into testtable2(id) values('"+tweet+"')")

            # print(tweet['text'])
            #
            # cursor.execute("insert into testtable2 (id) VALUES (%s)",(tweets['text']))
            # cursor.execute("insert into testtable2(id) values('"+tweet+"')")


if __name__ == "__main__":
    # calling main function
    main()