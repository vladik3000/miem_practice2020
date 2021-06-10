from time import sleep
from typing import Any

import pika.exceptions
import epicbox.exceptions
import requests.exceptions
import socket

from queue_configuration import rabbitmq_example

from config import CONNECTION_RETRY_TIME, QUEUE_CONFIG_NAME
from logs import get_logger
from broker.rabbitmq import (
    receive_messages as rabbitmq_receive,
)
def start_grader() -> None:
    logger = get_logger("start_grader")

    try:
        while True:
            listen_to_broker(rabbitmq_example)
            sleep(CONNECTION_RETRY_TIME)
    except AttributeError as exception:
        logger.error(exception, exc_info=True)
    except epicbox.exceptions.DockerError as exception:
        logger.error("Docker error: \n%s.", exception)
    except socket.gaierror:
        logger.error("Unknown host name in queue configuration file.")
    except KeyboardInterrupt:
        logger.info("Program has been stopped manually.")
    except Exception as exception:
        logger.error("Unhandled exception: \n%s.", exception, exc_info=True)


def listen_to_broker(queue_config: Any):
    """
    Listen to chosen message broker.

    :param queue_config: Module containing queue config.
    """
    logger = get_logger("start_grader")

    if queue_config.TYPE == "rabbitmq":
        try:
            rabbitmq_receive(
                queue_config.HOST,
                queue_config.PORT,
                queue_config.USER,
                queue_config.PASS,
                queue_config.QUEUE,
            )
        except pika.exceptions.AMQPConnectionError as exception:
            logger.error("Failed to connect to RabbitMQ broker. %s", exception)
    else:
        logger.error("Unknown message broker type: %s", queue_config.TYPE)

start_grader()
