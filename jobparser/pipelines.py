# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['vacancies_python']

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        salary = self.process_salary(item.pop('salary'))
        item['salary_min'] = salary[0]
        item['salary_max'] = salary[1]
        collection.insert_one(item)
        return item

    def process_salary(self, salary):
        if salary[0] == "от":
            salary_min = salary[2]
            salary_max = None
        elif salary[0] == "до":
            salary_max = salary[2]
            salary_min = None
        elif len(salary) == 1:
            salary_min = None
            salary_max = None
        elif len(salary) == 3:
            salary_min = salary[0] + ' ' + salary[2]
            salary_max = salary[0] + ' ' + salary[2]
        elif len(salary) == 4:
            salary_min = salary[0] + ' ' + salary[3]
            salary_max = salary[1] + ' ' + salary[3]
        elif len(salary) == 5 and salary[0] == "от ":
            salary_min = None
            salary_max = salary[1] + ' ' + salary[3]
        elif len(salary) == 5 and salary[0] == "от ":
            salary_min = salary[1] + ' ' + salary[3]
            salary_max = None
        elif len(salary) > 5:
            salary_min = salary[1] + ' ' + salary[5]
            salary_max = salary[3] + ' ' + salary[5]

        salary = [salary_min, salary_max]

        return salary
