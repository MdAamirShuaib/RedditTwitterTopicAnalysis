import praw
import pandas as pd
from praw.models import MoreComments
import re


def get_comments(url, client_id, client_secret, user_agent):
    post_comments = []
    try:
        reddit = praw.Reddit(
            client_id=client_id, client_secret=client_secret, user_agent=user_agent
        )
        submission = reddit.submission(url=url)
        for comment in submission.comments:
            if type(comment) == MoreComments:
                continue
            post_comments.append(re.sub("[^0-9a-zA-Z\s]+", " ", comment.body))
        return post_comments
    except:
        return post_comments


def get_reddit(query, client_id, client_secret, user_agent, count: int = 100):
    print("Extracting Data from Reddit Posts for " + query)
    reddit = praw.Reddit(
        client_id=client_id, client_secret=client_secret, user_agent=user_agent
    )
    subreddit = reddit.subreddit(query)
    posts = subreddit.hot(limit=count)

    posts_dict = {
        "Title": [],
        "PostText": [],
        "ID": [],
        "Score": [],
        "Total Comments": [],
        "PostURL": [],
    }

    for post in posts:
        posts_dict["Title"].append(re.sub("[^0-9a-zA-Z\s]+", "", post.title))
        posts_dict["PostText"].append(re.sub("[^0-9a-zA-Z\s]+", "", post.selftext))
        posts_dict["ID"].append(post.id)
        posts_dict["Score"].append(post.score)
        posts_dict["Total Comments"].append(post.num_comments)
        posts_dict["PostURL"].append(post.url)

    top_posts = pd.DataFrame(posts_dict)
    top_posts["Comments"] = top_posts["PostURL"].apply(
        lambda x: get_comments(x, client_id, client_secret, user_agent)
    )

    print("Reddit Extraction for " + query + " is complete")
    return top_posts
