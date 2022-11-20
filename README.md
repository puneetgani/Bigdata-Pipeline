
# Bigdata Pipeline

This project provides an insight about how one can go about creating a bigdata pipeline. 
In this project I have emulated a microservice using a python script which sends post request 
to a Producer Api, the messages are then written to a data streaming platfrom called kafka and later the 
consumer Api writes the messages to a clickhouse database.


![dataFlow](https://user-images.githubusercontent.com/106878112/202919049-fd023444-f9b4-4936-b497-d04f6d12e9f2.png)


## Tech Stack

**Python :** ( Modules used : fastapi, requests, kafka-python, clickhouse-driver, faker )

**Kafka :** data streaming platform.

**Docker :** containerisation technology.

**Clickhouse :** one of the fastest database in the world.


## Producer Application

The Producer Api sends all the json data sent in a post request to a perticular topic in a kafka broker.

Read the documentation of all the modules used in this program to understand the code written here in an efficient way.

```python
import json
from random import randrange
from fastapi import FastAPI, status
from kafka import KafkaProducer
from pydantic import BaseModel


def json_serializer(data):
    return json.dumps(data).encode('utf-8')


producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=json_serializer)

app = FastAPI()


class Post(BaseModel):
    name: str
    address: str
    created_at: str


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(1, 10000)
    producer.send("topic-name", post_dict)
    return post_dict

```


## Microservice Emulator

I have written a python script to emulate a fake data and send it using a post request to my desired url.

Read the documentation of all the modules used in this program to understand the code written here in an efficient way.

```python
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

```



## Cosumer Application

The Consumer Api sends all the json data sent to a perticular topic in a kafka broker to the clickhouse database .

Read the documentation of all the modules used in this program to understand the code written here in an efficient way.

```python
from clickhouse_driver import Client
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "<topic-name>",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset="latest",
    enable_auto_commit=True)


client = Client(host='localhost')

for message in consumer:
    a = str(message.value)
    b = (a[2:(len(a)-1)])
    c = (json.loads(b))
    name = c['name']
    address = c['address']
    created_at = c['created_at']
    client.execute(f"INSERT INTO <table-name> (name, address, created_at) values('{name}',
    '{address}','{created_at}')")

```

## 🚀 About Me
I'm a Data Engineer who is very passionate about solving data problems.
I'm passionate about learning new stuff, do reach out to me. 

## 🔗 Links
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/puneetgani)


