import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
DATABASE_HOST = os.environ.get("DATABASE_HOST")
DATABASE_PORT = int(os.environ.get("DATABASE_PORT"))
client = MongoClient(DATABASE_HOST, DATABASE_PORT)
roulette_database = client["roulette_database"]
bets_collection = roulette_database["bets_collection"]
spins_collection = roulette_database["spins_collection"]
users_collection = roulette_database["users_collection"]


def initialize_database():
    if spins_collection.find().retrieved == 0:
        spins_collection.insert_one({"id": 0})
