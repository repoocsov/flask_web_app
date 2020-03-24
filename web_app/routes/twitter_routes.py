# web_app/routes/twitter_routes.py
from flask import Blueprint, render_template, redirect, request, jsonify
from web_app.models import db, User, Tweet
from web_app.services.twitter_service import twitter_api_client
from web_app.services.basilica_service import basilica_api_client

twitter_routes = Blueprint("twitter_routes", __name__)


# FORM TO FIND USERS TWEETS
@twitter_routes.route("/twitter/find_user")
def find_user():
    return render_template("find_user.html", message="")


# DISPLAYS THE SEARCHED USER TWEETS USING TWITTER API AND STORES THEM
# ALSO STORES TWEETS IN BASILICA FORMAT USING BASILICA API
@twitter_routes.route("/twitter/find_user/display", methods=['POST'])
def save_and_return_user():
    # GETTING USER FROM FORM
    searched_user = request.form["user"]

    # USING TWITTER SERVICE
    api = twitter_api_client()
    twitter_user = api.get_user(searched_user)
    statuses = api.user_timeline(searched_user, tweet_mode="extended", count=100, exclude_replies=True, include_rts=False)

    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)
    db_user.screen_name = twitter_user.screen_name
    db_user.name = twitter_user.name
    db_user.location = twitter_user.location
    db_user.followers_count = twitter_user.followers_count
    db.session.add(db_user)
    db.session.commit()

    # USING BASILICA SERVICE
    basilica_api = basilica_api_client()
    all_tweet_texts = [status.full_text for status in statuses]
    embeddings = list(basilica_api.embed_sentences(all_tweet_texts, model="twitter"))

    counter = 0
    for status in statuses:
        db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
        db_tweet.user_id = status.author.id
        db_tweet.full_text = status.full_text

        embedding = embeddings[counter]
        db_tweet.embedding = embedding
        db.session.add(db_tweet)
        counter+=1
    db.session.commit()

    return render_template("display_user.html", user=searched_user)


# DISPLAYS ONE USER
@twitter_routes.route("/twitter/<id>")
def get_user(id=None):
    tweets = Tweet.query.filter_by(user_id=id).all()
    user = User.query.filter_by(id=id).all()
    return render_template("specific_user_tweets.html", tweets=tweets, user=user)


# DISPLAYS ALL USERS
@twitter_routes.route("/twitter/all_users")
def all_users():
    users = User.query.all()
    return render_template("all_users.html", users=users)