from typing import Any, Dict
from datetime import datetime
from time import sleep
import json
import uuid
import logging

from exceptions import InvalidJSONException
from queue_configuration.rabbitmq_example import {
        HOST,
        PORT,
        USER,
        PASS)

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

class MessageHandler(object):
    """
    Бот для проверки заданий на внешнем грейдере.

    Команды бота:
    '@**External Grader**' — описание и список команд.
    '@**External Grader** grade <id задания> <ответ>' — проверка задания.
    """
    def __init__(self, message):
        self.config = {}
        self.config["host"] = 
        self.create_queue_connection()
        self.response = str()
    # noinspection PyAttributeOutsideInit
    def initialize(
            self,
            bot_handler: Any
    ) -> None:
        self.bot_handler = bot_handler
        self.config = bot_handler.get_config_info('rabbitmq')
        self.gradings = {}
        self.response = {}

        self.create_queue_connection()

    # noinspection PyAttributeOutsideInit
    def create_queue_connection(self):
        # RabbitMQ RPC
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.config["host"],
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

    def usage(self):
        return """
        Бот для проверки заданий на внешнем грейдере.
        
        Команды бота:
        '@**External Grader**' — описание и список команд.
        '@**External Grader** grade <id задания> <ответ>' — проверка задания.
        """

    def handle_message(
            self,
            message: Dict[str, str],
            bot_handler: Any
    ) -> None:
        """
        Handle messages.

        :param message: Message from user.
        :param bot_handler: ?
        """
        bot_response = ""
        content = message["content"]
        words = content.split(sep=None, maxsplit=2)

        logging.getLogger().info("Received message '{0}' from '{1}'.".format(
            content, message["sender_full_name"])
        )

        if not words or words[0] == "help":
            bot_response = (
                "Бот для проверки заданий.\n"
                "\n"
                "Команды бота:\n"
                "'@**External Grader**' — описание и список команд.\n"
                "'@**External Grader** grade <id задания> <ответ>' — проверка задания.\n"
            )
        elif words[0] == "grade":
            if len(words) != 3:
                bot_response = (
                    "Ошибка. Ожидаемый формат команды:\n"
                    "\n"
                    "'@**External Grader** grade <id задания> <ответ>'\n"
                )
            else:
                self.bot_handler.send_reply(
                    message,
                    "Пожалуйста, подождите. Ответ проверяется внешним сервисом.\n"
                )

                # Grading the answer
                self.rabbitmq_grade_answer(
                    words[1],
                    words[2],
                    message
                )
        else:
            bot_response = (
                "Неизвестная команда.\n"
                "\n"
                "Наберите '@**External Grader**' для получения справки.\n"
            )

        if bot_response:
            self.bot_handler.send_reply(message, bot_response)

    def rabbitmq_grade_answer(
            self,
            script_id: str,
            answer: str,
            message: Dict[str, str]
    ) -> None:
        """
        Send student answer to RabbitMQ queue for grading.

        :param script_id: ID of the script.
        :param answer: Student answer.
        :param message: Message object.
        """
        corr_id = str(uuid.uuid4())
        self.response[corr_id] = None

        payload = {
            "xqueue_header": {
                "submission_key": datetime.timestamp(datetime.now())
            },
            "xqueue_body": {
                "student_response": answer,
                "grader_payload": script_id
            }
        }

        logging.getLogger().info("Sending message {0} to RabbitMQ.".format(json.dumps(payload)))

        self.gradings[payload["xqueue_header"]["submission_key"]] = message

        # Attempt to send message 3 times
        for i in range(3):
            logging.getLogger().info("Connecting to RabbitMQ. Attempt {0} / 3.".format(i + 1))

            try:
                self.channel.basic_publish(
                    exchange='',
                    routing_key=self.config["queue"],
                    properties=pika.BasicProperties(
                        reply_to=self.callback_queue,
                        correlation_id=corr_id
                    ),
                    body=json.dumps(payload)
                )

                logging.getLogger().info("Message sent. Awaiting answer.")

                break
            except Exception as exception:
                if i == 2:
                    raise exception

                self.create_queue_connection()

        while self.response[corr_id] is None:
            self.connection.process_data_events()

    def on_callback(
            self,
            current_channel: pika.channel.Channel,
            basic_deliver: pika.spec.Basic.Deliver,
            properties: pika.spec.BasicProperties,
            body: bytes
    ):
        logging.getLogger().info("Received message from RabbitMQ.")

        self.response[properties.correlation_id] = body

        msg = json.loads(self.response[properties.correlation_id].decode("utf8"))
        message = self.gradings[msg["xqueue_header"]["submission_key"]]
        self.reponse = message
        bot_response = (
            "@**" + message["sender_full_name"] + "**\n"
            "\n"
            "Оценка:\n"
            "```\n" + str(msg["xqueue_body"]["score"]) + "\n```\n"
            "Сообщение:\n"
            "```\n" + str(msg["xqueue_body"]["msg"]) + "\n```"
        )

        self.bot_handler.send_reply(message, bot_response)


#handler_class = ExternalGraderHandler
