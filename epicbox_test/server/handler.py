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
        self.response = str()
        self.create_queue_connection()
    # noinspection PyAttributeOutsideInit
    #def initialize(
    #        self,
    #        bot_handler: Any
    #) -> None:
    #    self.bot_handler = bot_handler
    #    self.config = bot_handler.get_config_info('rabbitmq')
    #    self.gradings = {}
    #    self.response = {}

    #    self.create_queue_connection()

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

    def handle_message(
            self,
            message: Dict[str, str]#,
            #bot_handler: Any
    ) -> None:
        pass
        #bot_response = ""
        #content = message["content"]
        #words = content.split(sep=None, maxsplit=2)

        #logging.getLogger().info("Received message '{0}' from '{1}'.".format(
        #    content, message["sender_full_name"])
        #)

        #if not words or words[0] == "help":
        #    bot_response = (
        #        "Бот для проверки заданий.\n"
        #        "\n"
        #        "Команды бота:\n"
        #        "'@**External Grader**' — описание и список команд.\n"
        #        "'@**External Grader** grade <id задания> <ответ>' — проверка задания.\n"
        #    )
        #elif words[0] == "grade":
        #    if len(words) != 3:
        #        bot_response = (
        #            "Ошибка. Ожидаемый формат команды:\n"
        #            "\n"
        #            "'@**External Grader** grade <id задания> <ответ>'\n"
        #        )
        #    else:
        #        self.bot_handler.send_reply(
        #            message,
        #            "Пожалуйста, подождите. Ответ проверяется внешним сервисом.\n"
        #       )

                # Grading the answer
        #self.rabbitmq_grade_answer(message)
        #else:
        #    bot_response = (
        #        "Неизвестная команда.\n"
        #        "\n"
        #        "Наберите '@**External Grader**' для получения справки.\n"
        #    )

        if bot_response:
            self.bot_handler.send_reply(message, bot_response)

    def rabbitmq_grade_answer(
            self,
            #script_id: str,
            #answer: str,
            message: Dict[str, str]
    ) -> None:
        corr_id = str(uuid.uuid4())
        self.response = None
        print("GRADING")
        payload = {
            "header": {
                "submission_time": datetime.timestamp(datetime.now())
            },
            "body": {
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
            print("piZda")
            self.connection.process_data_events()

    def on_callback(
            self,
            current_channel: pika.channel.Channel,
            basic_deliver: pika.spec.Basic.Deliver,
            properties: pika.spec.BasicProperties,
            body: bytes
    ):
        logging.getLogger().info("Received message from RabbitMQ.")
        print("RECIEVED MESSAGE FROM RABBITMQ")
        #self.response[properties.correlation_id] = body
        self.response = str(body.decode()) # change it ofc 
        print("SELF.RESPONSE", self.response)
        #msg = json.loads(self.response[properties.correlation_id].decode("utf8"))
        #message = self.gradings[msg["xqueue_header"]["submission_key"]]
        #self.reponse = message
        #bot_response = (
        #    "@**" + message["sender_full_name"] + "**\n"
        #    "\n"
        #    "Оценка:\n"
        #    "```\n" + str(msg["xqueue_body"]["score"]) + "\n```\n"
        #    "Сообщение:\n"
        #    "```\n" + str(msg["xqueue_body"]["msg"]) + "\n```"
        #)
        #self.bot_handler.send_reply(message, bot_response)

#handler_class = ExternalGraderHandler
