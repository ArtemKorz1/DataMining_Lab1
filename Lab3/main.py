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

        if type(json_list) is list:
            for item in json_list:
                if not collection.find_one({p_key: item[p_key]}):
                    collection.insert_one(item)
        elif type(p_key) is list:
            accept = True
            ones = list(collection.find({p_key[0]: json_list[p_key[0]]}))
            for one in ones:
                isIdentical = True
                for key in p_key:
                    if key != '_id' and one[key] != json_list[key]:
                        isIdentical = False
                if isIdentical:
                    accept = False
                    break
            if accept:
                collection.insert_one(json_list)
        elif not collection.find_one({p_key: json_list[p_key]}):
            collection.insert_one(json_list)

    def is_empty(self, coll_name=''):
        collection = self.collection_by_name(coll_name)

        return collection.estimated_document_count() == 0

    def drop(self, coll_name=''):
        collection = self.collection_by_name(coll_name)

        collection.drop()

    def save_to_Json(self, coll_name='', file_name=''):
        collection = self.collection_by_name(coll_name)

        found = collection.find().to_list()
        restricted = ["_id"]
        items = JsonWork.choose_not(found, restricted)

        JsonWork.save(file_name, items)
