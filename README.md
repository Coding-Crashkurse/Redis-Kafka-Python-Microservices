# Redis-Kafka-Python-Microservices

This Repository contains multiple microservices which make use of Kafka and Redis.

Three services are there to manipulate data. The data gets stored in redis and the corresponding key gets stored in a topic, where the "child" service is subscribed. When the producer writes something to a topic, the consumer gets the key and gets the value from redis, transforms it and so on. This creates a chain of microservices, each with a specific task.

1. Apiservice: RestAPI to create a string
2. Middleservice: Capitalize string
3. Endservice: Uppercase string

Run it yourself:

`docker-compose up --build`

Go to `localhost:8000/docs` and use to the ui to send data.
