from .auth_token import *

from dataclasses import dataclass
from datetime import datetime


@dataclass
class HopUser:
    printable_headers = ['UUID', 'Email', 'Provider',
                         "Register Date", "Last Login", "Is Anonimous"]

    registerTs: datetime
    provider: str
    uuid: str
    email: str
    lastLoginTs: datetime = None
    password: str = None
    name: str = None
    projects: list = None
    picture: str = None
    locale: str = None
    idToken: Token = None
    isAnonymous: bool = False

    @classmethod
    def fromJson(cls, json):
        return cls(
            datetime.strptime(json["registerTs"], '%Y-%m-%d %H:%M:%S.%f'),
            json["provider"],
            json["uuid"],
            json["email"],
            lastLoginTs=datetime.strptime(json["lastLoginTs"], '%Y-%m-%d %H:%M:%S.%f') if
            "lastLoginTs" in json else None,
            password=json["password"] if "password" in json else None,
            name=json["name"] if "name" in json else None,
            projects=json["projects"] if "projects" in json else [],
            picture=json["picture"] if "picture" in json else None,
            locale=json["locale"] if "locale" in json else None,
            idToken=Token(json["idToken"]) if "idToken" in json else None,
            isAnonymous=json["isAnonymous"] if "isAnonymous" in json else None,
        )

    @property
    def printable(self):
        return [self.uuid, self.email, self.provider, self.registerTs, self.lastLoginTs, self.isAnonymous]


@dataclass
class UserSnapshot:
    user: HopUser
    success: bool = True
    reason: str = ""


class UserReference:
    def __init__(self, docs, id):
        self._docs = docs
        self.id = id

    def get(self):
        return self._docs.index(".hop.auth").document(self.id).get()

    def delete(self):
        return self._docs.index(".hop.auth").document(self.id).delete()
