from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1', 27017)

db = client['vacancy_list']
jobs = db.jobs


def salary(value):
    for item in db.jobs({'$or': [{'salary_min': {'$gt': value}}, {'salary_max': {'$gt': value}}]}):
        pprint(item)


salary(100000)
