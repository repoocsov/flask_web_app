# web_app/routes/twitter_routes.py
from flask import Blueprint, render_template, redirect, request, jsonify
from web_app.models import db, User, Tweet
from web_app.services.twitter_service import twitter_api_client
from web_app.services.basilica_service import basilica_api_client
from sklearn.linear_model import LogisticRegression

twitter_routes = Blueprint("twitter_routes", __name__)

# FUNCTION TO GET AND STORE A TWITTER USERS DATA
def store_twitter_user_data(screen_name):
    api = twitter_api_client()
    twitter_user = api.get_user(screen_name)
    statuses = api.user_timeline(screen_name, tweet_mode="extended", count=150)

    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)
    db_user.screen_name = twitter_user.screen_name
    db_user.name = twitter_user.name
    db_user.location = twitter_user.location
    db_user.followers_count = twitter_user.followers_count
    db.session.add(db_user)
    db.session.commit()

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

    return db_user, statuses


# FORM TO FIND USERS TWEETS
@twitter_routes.route("/twitter/find_user")
def find_user():
    return render_template("find_user.html", message="")


# DISPLAYS THE SEARCHED USER 
@twitter_routes.route("/twitter/find_user/display", methods=['POST'])
def save_and_return_user():
    # GETTING USER FROM FORM
    searched_user = request.form["user"]
    store_twitter_user_data(searched_user)

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


# FORM TO PREDICT WHO AUTHORED A TWEET
@twitter_routes.route("/twitter/predict")
def predict():
    users = User.query.all()
    return render_template("predict.html", users=users)

# GET RESULTS OF FORM
@twitter_routes.route("/twitter/results", methods=["POST"])
def results():
    screen_name_a = request.form["screen_name_a"]
    screen_name_b = request.form["screen_name_b"]
    tweet_text = request.form["tweet_text"]

    user_a = User.query.filter(User.screen_name == screen_name_a).one()
    user_b = User.query.filter(User.screen_name == screen_name_b).one()
    user_a_tweets = user_a.tweets
    user_b_tweets = user_b.tweets

    embeddings = []
    labels = []
    for tweet in user_a_tweets:
        labels.append(user_a.screen_name)
        embeddings.append(tweet.embedding)

    for tweet in user_b_tweets:
        labels.append(user_b.screen_name)
        embeddings.append(tweet.embedding)

    classifier = LogisticRegression(random_state=0, solver='lbfgs')
    classifier.fit(embeddings, labels)

    basilica_conn = basilica_api_client()
    example_embedding = basilica_conn.embed_sentence(tweet_text, model="twitter")
    result = classifier.predict([example_embedding])

    return render_template("results.html",
        screen_name_a=screen_name_a,
        screen_name_b=screen_name_b,
        tweet_text=tweet_text,
        screen_name_most_likely=result[0]
    )