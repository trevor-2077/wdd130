import os
from dotenv import load_dotenv

load_dotenv()  # load vars from .env

class Config:
    # Pulls in DATABASE_URL, e.g.
    # mysql+pymysql://trevor:2243@localhost/smith_food_storage_db
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
