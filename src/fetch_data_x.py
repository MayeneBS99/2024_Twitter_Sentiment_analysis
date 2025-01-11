import csv
from configparser import ConfigParser
from random import randint
from datetime import datetime
import time
import asyncio
from twikit import Client, TooManyRequests

MINIMUM_TWEETS = 1500
QUERY = 'england 2024 lang:en until:2024-05-31 since:2024-03-01'

async def get_tweets(client, tweets):
    if tweets is None:
        # get tweets
        print(f'{datetime.now()} - Getting tweets....')
        tweets = await client.search_tweet(QUERY, product='Top')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting Next tweets after {wait_time} seconds...')
        await asyncio.sleep(wait_time)  # Utiliser asyncio.sleep pour éviter de bloquer l'exécution
        tweets = await tweets.next()

    return tweets

async def fetch_and_save_tweets():
    # login credentials
    config = ConfigParser()
    config.read('C:/Users/mayen/PROJET_IEF2I/src/config.ini')
    username = config['X']['username']
    email = config['X']['email']
    password = config['X']['password']

    # creating a csv file
    with open('tweets_england_0305.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Tweet_count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes'])

    # authenticate to X.com
    client = Client(language='en-EN')
    client.load_cookies(r'C:\Users\mayen\PROJET_IEF2I\src\cookies.json')

    tweet_count = 0
    tweets = None

    while tweet_count < MINIMUM_TWEETS:
        try:
            tweets = await get_tweets(client, tweets)  # Passer client comme paramètre
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'{datetime.now()} - Rate Limit reached. Waiting until {rate_limit_reset}')
            wait_time = (rate_limit_reset - datetime.now()).total_seconds()
            await asyncio.sleep(wait_time)
            continue

        if not tweets:
            print(f'{datetime.now()} - No more tweets found')
            break

        for tweet in tweets:
            tweet_count += 1
            tweet_data = [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]
            with open('tweets_england_0305.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data)

        print(f'{datetime.now()} - Got {tweet_count} tweets')

    print(f'{datetime.now()} - Done! Got {tweet_count} tweets in total')

# Exécuter la fonction asynchrone
if __name__ == "__main__":
    asyncio.run(fetch_and_save_tweets())
