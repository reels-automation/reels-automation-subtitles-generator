import logging
from quixstreams import Application

def create_producer(app_producer:Application, topic_to_produce:str,key:str,data:str):
    with app_producer.get_producer() as producer:
        producer.produce(
            topic=topic_to_produce,
            key = key,
            value = data
        )
    logging.info("Produced. Sleeping..")