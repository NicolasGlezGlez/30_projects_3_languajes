from fastapi import FastAPI, Header
from pydantic import BaseModel
from app import decode_jwt
from mongodb import save_tweet, get_all_tweets
from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime

app = FastAPI()


class Tweet(BaseModel):
    content: str


class TweetOut(BaseModel):
    _id: str
    content: str
    timestamp: datetime

    class Config:
        json_encoders = {
            ObjectId: str
        }


@app.post("/post_tweet/")
async def post_tweet(tweet: Tweet, authorization: str = Header(...)):
    print("Tweet: ", tweet)
    user_data = decode_jwt(authorization.split(" ")[1])
    print("user_data: ", user_data)
    user_id = user_data["_id"]
    save_tweet(user_id, tweet.content)
    print("save_tweet: ", save_tweet)
    return {"tweet": tweet.content, "user_id": user_id}


@app.get("/get_tweets/")
async def get_tweets():
    tweets = get_all_tweets()
    for tweet in tweets:
        tweet["_id"] = str(tweet["_id"])
    return tweets

