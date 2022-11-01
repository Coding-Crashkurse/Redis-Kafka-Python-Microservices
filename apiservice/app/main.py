from typing import Union
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka import Producer
from fastapi import FastAPI
from pydantic import BaseModel
import redis
import uuid
import time

time.sleep(60)

admin = AdminClient({'bootstrap.servers': 'kafka:9092'})
producer = Producer({'bootstrap.servers': 'kafka:9092'})
r = redis.Redis(host="redis", port=6379, db=1, password="mysecretpw")


new_topic = NewTopic("topic1", num_partitions=3, replication_factor=1)
new_topic2 = NewTopic("topic2", num_partitions=3, replication_factor=1)

fs = admin.create_topics([new_topic, new_topic2])

class Message(BaseModel):
    description: str

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    for topic, f in fs.items():
        try:
            f.result()
            print(f"Topic {topic} wurde erstellt")
        except Exception as e:
            print(f"Error: Topic {topic} konnte nicht erstellt werden: {e}")

@app.post("/")
def create_message(message: Message):
    new_id = str(uuid.uuid4())
    producer.produce('topic1', new_id.encode('utf-8'))
    new_message = message.description.capitalize()
    r.set(new_id, new_message)
    producer.flush()
    return {"message": message.description}