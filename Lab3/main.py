from pymongo import MongoClient

from Lab1.main import JsonWork

lab3_suffix = 'Lab3\\'
coll_name_default = 'Tl_Perm'


class MongoWork:
    def __init__(self, host='localhost', port=27017, db_name='data_mining', coll_name=coll_name_default):
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.coll = self.db[coll_name]

    def collection_by_name(self, coll_name=''):
        if coll_name != '':
            collection = self.db[coll_name]
        else:
            collection = self.coll

        return collection

    def save(self, json_list, coll_name=''):
        collection = self.collection_by_name(coll_name)

        if type(json_list) is list:
            collection.insert_many(json_list)
        else:
            collection.insert_one(json_list)

    def resave(self, json_list, coll_name=''):
        if not self.is_empty(coll_name):
            self.drop(coll_name)
        self.save(json_list, coll_name)

    def add(self, json_list, p_key, coll_name=''):
        collection = self.collection_by_name(coll_name)

        for item in json_list:
            if not collection.find_one({p_key: item[p_key]}):
                collection.insert_one(item)

    def is_empty(self, coll_name=''):
        collection = self.collection_by_name(coll_name)

        return collection.estimated_document_count() == 0

    def drop(self, coll_name=''):
        collection = self.collection_by_name(coll_name)

        collection.drop()