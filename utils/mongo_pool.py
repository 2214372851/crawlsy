from pymongo import MongoClient
from pymongo.collection import Collection
from django.conf import settings


class MongoDBPool:
    def __init__(self):
        self._client = MongoClient(settings.MONGO_URL)
        self._db = self.client[settings.MONGO_DB]
        self._collection_map = {}

    @property
    def client(self):
        return self._client

    def collection(self, name: str) -> Collection:
        if name not in self._collection_map:
            self._collection_map[name] = self._db[name]
        return self._collection_map[name]


mongodb_pool = MongoDBPool()
