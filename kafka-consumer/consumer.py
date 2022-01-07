import datetime
import json
import logging
import os

from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import ConnectionError
from kafka import KafkaConsumer

ELASTIC_HOST = os.environ.get('ELASTIC_HOST', 'localhost')
ELASTIC_PORT = os.environ.get('ELASTIC_PORT', '9200')

KAFKA_HOST = os.environ.get('KAFKA_HOST', 'localhost')
KAFKA_PORT = os.environ.get('KAFKA_PORT', '9092')
KAFKA_API_VERSION = os.environ.get('KAFKA_API_VERSION', '2.5.0')

LOGGING_LEVEL = int(os.environ.get("LOGGING_LEVEL", logging.INFO))

# Topics and their corresponding indices have the same name
TOPICS_AND_INDEX = [
    'dataset',
    'reuse',
    'organization',
]


logging.basicConfig(level=LOGGING_LEVEL)


def create_elastic_client():
    logging.info('Creating Elastic Client')
    es = Elasticsearch([{'host': ELASTIC_HOST, 'port': ELASTIC_PORT}])
    logging.info('Elastic Client created')
    return es


def create_kafka_consumer():
    logging.info('Creating Kafka Consumer')
    consumer = KafkaConsumer(
        bootstrap_servers=f'{KAFKA_HOST}:{KAFKA_PORT}',
        group_id='elastic',
        reconnect_backoff_max_ms=100000, # TODO: what value to set here?
        
        # API Version is needed in order to prevent api version guessing leading to an error
        # on startup if Kafka Broker isn't ready yet
        api_version=tuple([int(value) for value in KAFKA_API_VERSION.split('.')])
        )
    consumer.subscribe(TOPICS_AND_INDEX)
    logging.info('Kafka Consumer created')
    return consumer


def consume_messages(consumer, es):
    logging.info('Ready to consume message')
    for message in consumer:
        value = message.value
        val_utf8 = value.decode('utf-8').replace('NaN','null')
        data = json.loads(val_utf8)
        key = message.key
        index = message.topic
        logging.info(f'Message recieved with key: {key} and value: {value}')

        if(val_utf8 != 'null'):
            data['created_at'] = datetime.datetime.fromisoformat(data['created_at'])
            try:
                es.update(index=index, id=key.decode('utf-8'), doc=data, doc_as_upsert=True)
            except ConnectionError as e:
                logging.error(f'ConnectionError with Elastic Client: {e}')
                # TODO: add a retry mechanism?
        else:
                try:
                    if(es.exists_source(index=index, id=key.decode('utf-8'))):
                        es.delete(index=index, id=key.decode('utf-8'))
                except ConnectionError as e:
                    logging.error(f'ConnectionError with Elastic Client: {e}')


def main():
    es = create_elastic_client()
    consumer = create_kafka_consumer()
    consume_messages(consumer, es)

if __name__ == '__main__':
    main()
