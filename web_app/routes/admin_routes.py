# web_app/routes/admin_routes.py

from flask import Blueprint, jsonify, request, render_template, flash, redirect
from web_app.models import db
from web_app.routes.twitter_routes import store_twitter_user_data

admin_routes = Blueprint("admin_routes", __name__)

@admin_routes.route("/admin/reset")
def reset_db():
    db.drop_all()
    db.create_all()
    return render_template("twitter.html", message="This is Twitter central. Either get a specific users tweets or display all past retrieved users and their tweets.")

@admin_routes.route("/admin/seed")
def seed_db():
    default_users = ["austen", "s2t2", "jack"]
    for screen_name in default_users:
        db_user, statuses = store_twitter_user_data(screen_name)

    return render_template("twitter.html", message="This is Twitter central. Either get a specific users tweets or display all past retrieved users and their tweets.")