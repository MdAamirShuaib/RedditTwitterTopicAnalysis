import tweepy as tw
import os
import pandas as pd


def get_tweets(
    query,
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
    count: int = 100,
):
    print("Extracting Data from Twitter on " + query)
    auth = tw.OAuthHandler(consumer_key, consumer_secret=consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)
    tweets = api.search_tweets(q=query, lang="en", count=count, tweet_mode="extended")

    users_locs = [
        [
            str(tweet.created_at),
            tweet.user.location,
            tweet.user.screen_name,
            tweet.retweeted_status.full_text
            if tweet.full_text.startswith("RT")
            else tweet.full_text,
            [hashs["text"] for hashs in tweet.entities["hashtags"]],
        ]
        for tweet in tweets
    ]
    twitterDf = pd.DataFrame(
        data=users_locs, columns=["datetime", "location", "user", "tweet", "hashtags"]
    )
    print("Twitter Extraction on " + query + " is complete")
    return twitterDf
