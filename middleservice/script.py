from confluent_kafka import Consumer, Producer
import logging
import time
import redis
import uuid
logging.basicConfig(level=logging.INFO)
time.sleep(60)

consumer = Consumer({
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
})
producer = Producer({'bootstrap.servers': 'kafka:9092'})
r = redis.Redis(host="redis", port=6379, db=1, password="mysecretpw")

consumer.subscribe(['topic1'])

def delivery_report(err, msg):
    if err is not None:
        print(f'Error in message: {err}')
    else:
        print(f'Message gesendet an to {msg.topic()} in partition {msg.partition()}')

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        logging.info(f"Consumer error: {msg.error()}")
        continue
    _id = msg.value().decode("utf-8")
    logging.info(f'Id in Middleservice erhalten: {_id}')
    message = r.get(_id).decode("utf-8")
    logging.info(f'Message in Middleservice erhalten: {message}')
    new_id = str(uuid.uuid4())
    r.set(new_id, message.upper())
    producer.poll(0)
    producer.produce('topic2', new_id.encode('utf-8'), callback=delivery_report)
