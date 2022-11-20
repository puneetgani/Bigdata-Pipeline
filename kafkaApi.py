import json
from random import randrange
from fastapi import FastAPI, status
from kafka import KafkaProducer
from pydantic import BaseModel


def json_serializer(data):
    return json.dumps(data).encode('utf-8')


producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=json_serializer)
"""
step1 : pip3 install kafka-python or pip install kafka-python

    bootstrap_servers=['localhost:9092']:sets the host and port, to which the producer should contact to bootstrap initial
    cluster metadata.It is not necessary to set this here,since the default is localhost:9092.

    value_serializer-lambdax:dumps(x).encode('utf-8'):function of how the data should be serialized before
    sending to the broker.Here,we convert the data to a json file and encode it to utf-8.
"""
app = FastAPI()


class Post(BaseModel):
    name: str
    address: str
    created_at: str


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(1, 10000)
    producer.send("puneet", post_dict)
    return post_dict
