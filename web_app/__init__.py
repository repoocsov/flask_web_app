# web_app/__init__.py

from flask import Flask
from web_app.models import db, migrate
import os
from dotenv import load_dotenv

from web_app.routes.home_routes import home_routes
from web_app.routes.twitter_routes import twitter_routes
from web_app.routes.admin_routes import admin_routes

load_dotenv()
DATABASE_URL = os.getenv("sqlite:///tweets.db", default="sqlite:///tweets.db")

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(twitter_routes)
    app.register_blueprint(home_routes)
    app.register_blueprint(admin_routes)

    return app

if __name__ == "__main__":
    app.config['DEBUG'] = False
    my_app = create_app()
