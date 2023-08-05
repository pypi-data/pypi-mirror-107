import requests
import urllib.parse
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Owner:

    id: str = None,
    display_name: str = None

    @classmethod
    def fromSoup(cls, soup):
        return cls(
            id=soup.find("id").text,
            display_name=soup.find("displayname").text
        )

    @property
    def json(self):
        return {"id": self.id, "display_name": self.display_name}


@dataclass
class Object:
    printable_headers = ["Id", "Last Modified",
                         "Size", "Owner", "Storageclass"]

    id: str
    data: bytes = b""
    url: str = None
    last_modified: datetime = None
    etag: str = None
    size: int = None
    owner: Owner = None
    storageclass: str = None

    @classmethod
    def fromSoup(cls, url, soup):
        last_modified = datetime.strptime(
            soup.find("lastmodified").text, '%Y-%m-%dT%H:%M:%S.%fZ')
        return cls(
            soup.find("key").text,
            url=url,
            last_modified=last_modified,
            etag=soup.find("etag").text.strip('"'),
            size=soup.find("size").text,
            owner=Owner.fromSoup(soup.find("owner")),
            storageclass=soup.find("storageclass").text
        )

    @property
    def json(self):
        return {"id": self.id, "url": self.url, "last_modified": self.last_modified, "etag": self.etag,
                "size": self.size, "owner": self.owner.json, "storageclass": self.storageclass}

    @property
    def printable(self):
        return [self.id, self.last_modified, self.size, self.owner.display_name, self.storageclass]


class ObjectSnapshot:
    def __init__(self, object, success=False):
        self.object = object
        self.success = success


class ObjectReference:
    def __init__(self, client, bucket, id):
        self.client = client
        self.bucket = bucket
        self.id = id

    def get(self):
        try:
            response = self.client.get(f"/{self.bucket}/{self.id}")
            return ObjectSnapshot(Object(self.id, data=response.content),
                                  success=True)
        except requests.exceptions.HTTPError:
            return ObjectSnapshot(None, success=False)

    def get_presigned(self):
        resource = f"/{self.bucket}/{self.id}"
        query = self.client.signer.getQuerySignature("GET", resource)
        return f"{self.client.base_url}{urllib.parse.quote(resource)}{query}"

    def put(self, data):
        try:
            response = self.client.put(f"/{self.bucket}/{self.id}", data)
            return ObjectSnapshot(Object(self.id, data=data), success=True)
        except requests.exceptions.HTTPError:
            return ObjectSnapshot(None, success=False)

    def delete(self):
        try:
            self.client.delete(f"/{self.bucket}/{self.id}")
            return True
        except requests.exceptions.HTTPError:
            return False
