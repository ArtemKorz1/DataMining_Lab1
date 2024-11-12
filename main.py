from pprint import pprint

from Lab1.main import Requestor
from Lab2.main import ParserTlPerm

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

