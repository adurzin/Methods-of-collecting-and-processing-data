from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client['instagram']
account = 'tgc1spb'  # account name (tgc1spb, teplosetspb)
user_type = 'following'  # following or follower

query_items = db[account].find({'user_type': user_type})
for item in query_items:
    print(item)
