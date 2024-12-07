from pprint import pprint

from Lab1.main import Requestor
from Lab2.main import ParserTlPerm
from Lab3.main import MongoWork
from Lab4.spiders.tl_spider import coll_name as coll_name_available
from Lab4.spiders.Experimental import coll_name as coll_name_protected
from Lab4.spiders.quotes_spider import coll_name as coll_name_quotes

#Lab1
Requestor.get_vk_groups()
Requestor.get_git_repos()

#Lab2-3
ParserTlPerm.get_stuff_by_xpath(True)
ParserTlPerm.get_stuff_by_bsoup()

#Lab3
#cost = input("Минимальная стоимость товара: ")
cost = 100
pprint(ParserTlPerm.choose_products_by_cost(cost))

#Lab4
#README.md
mongo = MongoWork()
mongo.save_to_Json(coll_name_available, 'Lab4\\items_from_mongoDB_spider.json')
mongo.save_to_Json(coll_name_protected, 'Lab4\\items_from_mongoDB_spider_protected.json')

#Lab5
#README.md
#mongo = MongoWork()
mongo.save_to_Json(coll_name_quotes, 'Lab5\\items_from_mongoDB_quotes_spider.json')
