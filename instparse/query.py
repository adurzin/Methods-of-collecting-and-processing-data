from pymongo import MongoClient
from pprint import pprint


client = MongoClient('localhost', 27017)
db = client['instagram']

user_for_query = 'tgc1spb'
query_follow = 'follower'

query = db[user_for_query].find({'user_type': query_follow})

for el in query:
    pprint(el)
