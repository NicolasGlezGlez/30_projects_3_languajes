from datetime import datetime
from pymongo import MongoClient
from werkzeug.security import check_password_hash

# Conexión a MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['twitter_clone']  # Aquí 'twitter_clone' es el nombre de tu base de datos
users_collection = db['users']
tweets_collection = db['tweets']


def save_tweet(user_id, content):
    """Guarda un nuevo tweet en la base de datos."""
    tweet_data = {
        "user_id": user_id,
        "content": content,
        "timestamp": datetime.utcnow()
    }
    tweets_collection.insert_one(tweet_data)


def get_all_tweets():
    """Recupera todos los tweets de la base de datos."""
    tweets = list(tweets_collection.find())
    for tweet in tweets:
        tweet["_id"] = str(tweet["_id"])
    return tweets



def save_user(user_data):
    """Guarda un nuevo usuario en la base de datos."""
    users_collection.insert_one(user_data)


def find_user_by_email(email):
    """Busca un usuario por su nombre de usuario."""
    return users_collection.find_one({"email": email})


def authenticate_user(email, password):
    user = find_user_by_email(email)
    if user and check_password_hash(user['password'], password):
        return user
    return None
