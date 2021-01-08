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
        self.mongo_base = client.vacancy_0201


    def process_item(self, item, spider):

        # item['new_field'] = 0         # не получится так добавить новое поле, идем в items.py
        # del item['new_field']         # Удаляем ненужное поле в item
        # item['salary_min'] = self.process_salary(item['salary'])
        collection = self.mongo_base[spider.name]

        item = prepare_item(item, spider)

        collection.insert_one(item)

        return item

    def process_salary(self, salary):
        pass


def prepare_item(item, spider):
    item['salary_min'] = None
    item['salary_max'] = None
    if spider.name == 'hhru':
        item['site'] = 'https://hh.ru/'

        if item['salary'][0] == 'от ':
            item['salary_min'] = int(re.sub('\D', '', item['salary'][1]))
            item['salary_max'] = int(re.sub('\D', '', item['salary'][3])) if item['salary'][0] > ' до ' else None
        elif item['salary'][0] == 'до ':
            item['salary_min'] = None
            item['salary_max'] = int(re.sub('\D', '', item['salary'][1]))
    else:
        item['site'] = 'https://www.superjob.ru/'

        if item['salary'][0] == 'от':
            item['salary_min'] = int(re.sub('\D', '', item['salary'][2]))
            item['salary_max'] = None
        elif item['salary'][0] == 'до':
            item['salary_min'] = None
            item['salary_max'] = int(re.sub('\D', '', item['salary'][2]))
        else:
            item['salary_min'] = int(re.sub('\D', '', item['salary'][0]))
            item['salary_max'] = int(re.sub('\D', '', item['salary'][1]))
    del item['salary']

    return item