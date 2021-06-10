from typing import Any, Dict
from datetime import datetime
from time import sleep
import json
import uuid
import logging
import sys
sys.path.append('..')
from queue_configuration.rabbitmq_example import HOST, PORT, USER, PASS, QUEUE

from logs import get_logger
import pika
import pika.channel
import pika.exceptions

def auth(message):
    #authentication?
    return True

def proccess_message(message):
    if not auth(message):
        return "Authentication failed :("
    handler = MessageHandler()
    try:
        handler.rabbitmq_grade_answer(message)
        return handler.response
    except KeyboardInterrupt:
        return "keyboard interrupt"
    return handler.response

class MessageHandler(object):
    def __init__(self):
        self.config = {}
        self.config['host'] = HOST
        self.config['port'] = PORT
        self.config['user'] = USER
        self.config['pass'] = PASS
        self.config['queue'] = QUEUE
        self.response = dict()
        self.create_queue_connection()
    # noinspection PyAttributeOutsideInit
    def create_queue_connection(self):
        # RabbitMQ RPC
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                #host=self.config["host"],
                host='localhost',
                port=self.config["port"],
                credentials=pika.credentials.PlainCredentials(
                    self.config["user"],
                    self.config["pass"]
                )
            )
        )
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_callback,
            auto_ack=True
        )

    def rabbitmq_grade_answer(
            self,
            message: Dict[str, str]
    ) -> None:
        corr_id = str(uuid.uuid4())
        self.response = None
        print("GRADING")
        payload = {
            "xqueue_header": {
                "submission_time": datetime.timestamp(datetime.now()),
                "name": message['name'],
                "work": message['work']
            },
            "xqueue_body": {
                "student_request": message,
            }
        }

        logging.getLogger().info("Sending message {0} to RabbitMQ.".format(json.dumps(payload)))

        #self.gradings[payload["xqueue_header"]["submission_key"]] = message

        # Attempt to send message 3 times
        for i in range(3):
            logging.getLogger().info("Connecting to RabbitMQ. Attempt {0} / 3.".format(i + 1))

            try:
                self.channel.basic_publish(
                    exchange='',
                    routing_key=self.config["queue"],
                    properties=pika.BasicProperties(
                        reply_to=self.callback_queue,
                        correlation_id=corr_id,
                    ),
                    body=json.dumps(payload)
                )

                logging.getLogger().info("Message sent. Awaiting answer.")

                break
            except Exception as exception:
                if i == 2:
                    raise exception

                self.create_queue_connection()

        while self.response is None:
            self.connection.process_data_events()

    def on_callback(
            self,
            current_channel: pika.channel.Channel,
            basic_deliver: pika.spec.Basic.Deliver,
            properties: pika.spec.BasicProperties,
            body: bytes
    ):
        logging.getLogger().info("Received message from RabbitMQ.")
        self.response = json.loads(body.decode())
