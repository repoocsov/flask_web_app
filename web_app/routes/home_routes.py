# web_app/routes/home_routes.py

from flask import Blueprint, render_template
from web_app.models import Tweet

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
def index():
    return render_template("layout.html")

@home_routes.route("/tweets")
def tweets():
    # SELECT * FROM tweets
    tweet_records = Tweet.query.all()
    print(tweet_records)
    return render_template("tweets.html", message="Some tweets", tweets=tweet_records)
