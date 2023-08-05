from .docs_document import DocumentReference, DocumentSnapshot, Document

import json
import requests
from enum import Enum
from dataclasses import dataclass


@dataclass
class Index:
    printable_headers = ['Name', 'Number of Docs']

    name: str
    num_docs: int
    status: str
    num_of_shards: int
    num_of_replicas: int
    active_primary_shards: int
    active_shards: int

    @classmethod
    def fromJson(cls, name, json, num_docs):
        return cls(
            name,
            num_docs,
            json["status"],
            json["number_of_shards"],
            json["number_of_replicas"],
            json["active_primary_shards"],
            json["active_shards"]
        )

    @property
    def printable(self):
        return [self.name, self.num_docs]


class QueryableReference:
    cachedIndex = {}

    def __init__(self, client, index):
        self.client = client
        self.index = index

    @property
    def compoundBody(self):
        return {
            "size": 100,
            "from": 0,
            "query": {
                "bool": {
                    "must": [],
                    "filter": []
                }
            }
        }

    def where(self, field, isEqualTo=None, isGreaterThan=None, isGreaterThanOrEqualTo=None,
              isLessThan=None, isLessThanOrEqualTo=None):
        return Query(self.client, self.index, self.compoundBody, field,
                     isEqualTo=isEqualTo,
                     isGreaterThan=isGreaterThan,
                     isGreaterThanOrEqualTo=isGreaterThanOrEqualTo,
                     isLessThan=isLessThan,
                     isLessThanOrEqualTo=isLessThanOrEqualTo)

    def get(self, size=100, fromm=0):
        data = self.compoundBody
        data["size"] = size
        data["from"] = fromm
        try:
            response = self.client.post(f"/{self.index}/_search", json=data)
            body = response.json()
            return IndexSnapshot(list(map(lambda doc: Document.fromJson(doc), body["hits"]["hits"])), success=True)
        except requests.exceptions.HTTPError as e:
            return IndexSnapshot([], success=False)

    def cachedToIndexSnapshot(self):
        return IndexSnapshot(list(self.cachedIndex.values), success=True)


class IndexSnapshot:
    def __init__(self, docs, success=False):
        self.docs = docs
        self.success = success


class IndexReference(QueryableReference):
    def __init__(self, client, index):
        super().__init__(client, index)

    def add(self, doc):
        try:
            response = self.client.post(f"/{self.index}/_doc", json=doc)
            body = response.json()
            return DocumentSnapshot(Document(doc, index=self.index, id=body["_id"], version=body["_version"]), success=True)
        except requests.exceptions.HTTPError as e:
            return DocumentSnapshot(None, success=False, reason=str(e))

    def setMapping(self, field, type, create=True):
        try:
            if create:
                self.client.put(f"/{self.index}")
        except:
            pass

        try:
            doc = {
                "properties": {
                    field: {
                        "type": type
                    }
                }
            }
            response = self.client.put(f"/{self.index}/_mapping", json=doc)
            return response.json()
        except requests.exceptions.HTTPError as e:
            return {"acknowledged": False}

    def document(self, id):
        return DocumentReference(self.client, self.index, id)

    @property
    def count(self):
        try:
            response = self.client.get(f"/{self.index}/_count")
            return response.json()["count"]
        except requests.exceptions.HTTPError:
            return 0

    def delete(self):
        try:
            self.client.delete(f"/{self.index}")
            return True
        except requests.exceptions.HTTPError:
            return True


class QueryType(Enum):
    IS_EQUAL_TO = 0
    IS_GREATER_THAN = 1
    IS_GREATER_THAN_OR_EQUAL_TO = 2
    IS_LESS_THAN = 3
    IS_LESS_THAN_OR_EQUAL_TO = 4


class Query(QueryableReference):
    def __init__(self, client, index, compoundQuery, field, isEqualTo=None, isGreaterThan=None, isGreaterThanOrEqualTo=None,
                 isLessThan=None, isLessThanOrEqualTo=None):
        super().__init__(client, index)

        self.compoundQuery = compoundQuery
        self.field = field

        if isEqualTo is not None:
            self.queryType = QueryType.IS_EQUAL_TO
            self.value = isEqualTo
        elif isGreaterThan is not None:
            self.queryType = QueryType.IS_GREATER_THAN
            self.value = isGreaterThan
        elif isGreaterThanOrEqualTo is not None:
            self.queryType = QueryType.IS_GREATER_THAN_OR_EQUAL_TO
            self.value = isGreaterThanOrEqualTo
        elif isLessThan is not None:
            self.queryType = QueryType.IS_LESS_THAN
            self.value = isLessThan
        elif isLessThanOrEqualTo is not None:
            self.queryType = QueryType.IS_LESS_THAN_OR_EQUAL_TO
            self.value = isLessThanOrEqualTo

    def equalToBody(self):
        return {"match": {self.field: self.value}}

    def comparisonBody(self, comparison):
        return {"range": {self.field: {comparison: self.value}}}

    @property
    def compoundBody(self):
        if self.queryType == QueryType.IS_EQUAL_TO:
            self.compoundQuery["query"]["bool"]["must"].append(
                self.equalToBody())

        elif self.queryType == QueryType.IS_GREATER_THAN:
            self.compoundQuery["query"]["bool"]["must"].append(
                self.comparisonBody("gt"))

        elif self.queryType == QueryType.IS_GREATER_THAN_OR_EQUAL_TO:
            self.compoundQuery["query"]["bool"]["must"].append(
                self.comparisonBody("gte"))

        elif self.queryType == QueryType.IS_LESS_THAN:
            self.compoundQuery["query"]["bool"]["must"].append(
                self.comparisonBody("lt"))

        elif self.queryType == QueryType.IS_LESS_THAN_OR_EQUAL_TO:
            self.compoundQuery["query"]["bool"]["must"].append(
                self.comparisonBody("lte"))

        return self.compoundQuery
