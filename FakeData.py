import json
import requests
from faker import Faker
import time

fake = Faker()


def user():
    return {
        "name": fake.name(),
        "address": fake.address(),
        "created_at": fake.year()
    }


if __name__ == '__main__':
    while 1 == 1:
        r = requests.post("http://127.0.0.1:8000/posts", data=json.dumps(user()))
        print(r.json())
        time.sleep(3)

