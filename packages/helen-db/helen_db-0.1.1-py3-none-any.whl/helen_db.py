# -*- coding: utf-8 -*-

from threading import Thread
import json
import time


class HELEN:
    def __init__(self, name: str = "db", interval=None, default=None):
        self.interval = 30 if not interval else interval
        self.default = {} if not default else default
        self.name = name

        try:
            with open(f"{self.name}.helen", "r+") as db:
                self.db = json.load(db)
        except FileNotFoundError:
            with open(f"{self.name}.helen", "w+") as db:
                json.dump({}, db)
            with open(f"{self.name}.helen", "r+") as db:
                self.db = json.load(db)

        Thread(target=self.save_interval).start()

    def get_user(self, user_id: int):
        return User(self.db[str(user_id)], str(user_id)) if str(user_id) in self.db \
            else UserCreate(self.db, str(user_id), self.default)

    def print(self, user_id: int = None):
        print(json.dumps(self.db[str(user_id)], indent=4)) if user_id else print(json.dumps(self.db, indent=4))

    def delete_user(self, user_id: int):
        del self.db[str(user_id)]

    def save(self):
        with open(f"{self.name}.helen", "w+") as db:
            json.dump(self.db, db, indent=4)
        print(f"NAME: {self.name} | USERS: {len(self.db)} | TIME: {int(time.time())}")

    def save_interval(self):
        while True:
            self.save()
            time.sleep(self.interval)


class User:
    def __init__(self, db: dict, user_id: str):
        self.user_id = user_id
        self.db = db

    def get(self, key: str = None):
        return self.db if not key else (self.db[key] if key in self.db else None)

    def lget(self, keys: list = None):
        return self.db if not keys else self.db[keys[0]][keys[1]]

    def set(self, key: str, value: any):
        self.db[key] = value

    def lset(self, keys: list, value: any):
        self.db[keys[0][keys[1]]] = value

    def plus(self, key: str, value: any):
        self.db[key] += value

    def lplus(self, keys: list, value: any):
        self.db[keys[0][keys[1]]] += value

    def minus(self, key: str, value: any):
        self.db[key] -= value

    def lminus(self, keys: list, value: any):
        self.db[keys[0][keys[1]]] -= value

    def print(self, key: str = None):
        print(self.get(key)) if key else print(json.dumps(self.db, indent=4))


class UserCreate(User):
    def __init__(self, db: dict, user_id: str, default=None):
        self.user_id = user_id
        self.db = db
        self.db[user_id] = default if default else {}
        super().__init__(self.db[user_id], self.user_id)
