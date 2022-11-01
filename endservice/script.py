from confluent_kafka import Consumer
import logging
import time
import redis
logging.basicConfig(level=logging.INFO)

time.sleep(60)

consumer = Consumer({
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['topic2'])
r = redis.Redis(host="redis", port=6379, db=1, password="mysecretpw")

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        logging.info(f"Consumer error: {msg.error()}")
        continue
    _id = msg.value().decode("utf-8")
    logging.info(f'Id in Endervice erhalten: {_id}')
    message = r.get(_id).decode("utf-8")
    logging.info(f'Message in Endservice erhalten: {message}')
