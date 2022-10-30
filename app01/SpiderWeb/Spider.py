import bs4
import requests
from lxml import etree

from app01 import header


class Spider:

    def __init__(self, url):
        self.resp = requests.get(url, headers=header.get_random_user_agents())
