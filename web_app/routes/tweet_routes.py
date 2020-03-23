# web_app/routes/tweet_routes.py

from flask import Blueprint, render_template, redirect, request, jsonify
from web_app.models import Tweet, db

tweet_routes = Blueprint("tweet_routes", __name__)


@tweet_routes.route("/tweets/new_tweet")
def tweets():
    return render_template("new_tweet.html", message="")


@tweet_routes.route("/tweets/create", methods=["POST"])
def create_tweet():
    # INSERT INTO tweets ...
    new_tweet = Tweet(content=request.form["content"], user_id=request.form["user_id"])
    print(new_tweet)
    db.session.add(new_tweet)
    db.session.commit()
    return redirect(f"/tweets")