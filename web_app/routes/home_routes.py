# web_app/routes/home_routes.py

from flask import Blueprint, render_template
from web_app.models import Tweet

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/index")
@home_routes.route("/")
def index():
    return render_template("layout.html")

@home_routes.route("/about")
def about():
    return render_template("about.html")

@home_routes.route("/twitter")
def twitter():
    return render_template("twitter.html", message="This is Twitter central. Either get a specific users tweets or display all past retrieved users and their tweets.")
