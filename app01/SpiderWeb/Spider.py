import httpx
import parsel as parsel
import requests

from app01 import header


class Spider:

    def __init__(self, url):
        self.resp = httpx.get(url, headers=header.get_random_user_agents())
        self.parser = parsel.Selector(self.resp.text)
