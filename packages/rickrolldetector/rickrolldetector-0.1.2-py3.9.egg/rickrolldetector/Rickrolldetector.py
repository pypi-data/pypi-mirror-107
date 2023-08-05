import requests
import re
import aiohttp

class RickRoleFinder:
    def __init__(self):
        self.cache = {}

    def find_rickroll(url):
        try:
            source = str(requests.get(url).content).lower()
            terms = ["rickroll","rick roll","rick astley","never gonna give you up"]
            return bool(re.findall("|".join(terms), source, re.MULTILINE))
        except:
            return
    async def async_find_rickroll(url):
        try:
            source = str(await(await super().get(url).content.read()))
            terms = ["rickroll","rick roll","rick astley","never gonna give you up"]
            return bool(re.findall('|'.join(terms), source, re.MULTILINE))
        except:
            return