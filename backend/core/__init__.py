from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_caching import Cache
from flask_restful import Api
from core.config import Config

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
app.app_context().push()

db=SQLAlchemy()
db.init_app(app)
cache = Cache(app)
