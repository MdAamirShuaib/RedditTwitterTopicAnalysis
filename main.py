from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from extractors.reddit import *
from extractors.youtube import *
from extractors.twitter import *
import analysis.generateWordCloud as generateWordCloud
import os
from dotenv import load_dotenv


load_dotenv()
app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/analyse", response_class=HTMLResponse)
async def analyse(request: Request, topic: str = Form(...), count: int = Form(10)):
    load_dotenv()
    client_id = os.environ["REDDIT_CLIENT_ID"]
    client_secret = os.environ["REDDIT_CLIENT_SECRET"]
    user_agent = os.environ["REDDIT_USER_AGENT"]

    consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
    consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
    access_token = os.environ["TWITTER_ACCESS_TOKEN"]
    access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

    short_topic = topic.replace(" ", "")
    print(short_topic)
    reddit_df = get_reddit(short_topic, client_id, client_secret, user_agent, count)
    twitter_df = get_tweets(
        topic, consumer_key, consumer_secret, access_token, access_token_secret, count
    )
    print(reddit_df, twitter_df)

    redditText = ""
    twitterText = ""

    for index, post in reddit_df.iterrows():
        redditText += post["Title"] + " " + post["PostText"]
        if post["Comments"]:
            redditText += " " + ", ".join(post["Comments"])

    for index, post in twitter_df.iterrows():
        twitterText += post["tweet"]

    Redditwordcloud = generateWordCloud.word_cloud(redditText)
    Twitterwordcloud = generateWordCloud.word_cloud(twitterText)

    return templates.TemplateResponse(
        "analysis.html",
        {
            "request": request,
            "redditWordCloud": Redditwordcloud,
            "twitterWordCloud": Twitterwordcloud,
            "topic": topic,
        },
    )
