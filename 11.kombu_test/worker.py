#!/usr/bin/env python
# coding=utf-8
# Author: zhuyuan

from __future__ import absolute_import, unicode_literals
from kombu.mixins import ConsumerMixin
from kombu.log import get_logger
from public import task_queues

logger = get_logger(__name__)


class Worker(ConsumerMixin):
    def __init__(self, connection):
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [
            Consumer(queues=task_queues["low"], accept=["pickle", "json"], callbacks=[self.task_low]),
            Consumer(queues=task_queues["mid"], accept=["pickle", "json"], callbacks=[self.task_mid]),
            Consumer(queues=task_queues["high"], accept=["pickle", "json"], callbacks=[self.task_high]),
            Consumer(queues=task_queues.values(), accept=["pickle", "json"], callbacks=[self.task_all]),
        ]

    def task_low(self, body, message):
        print "task_low: body: %s", body
        message.ack()

    def task_mid(self, body, message):
        print "task_mid: body: %s", body
        message.ack()

    def task_high(self, body, message):
        print "task_high: body: %s", body
        message.ack()

    def task_all(self, body, message):
        print "task_all: body: %s", body
        message.ack()


if __name__ == '__main__':
    from kombu import Connection
    from kombu.utils.debug import setup_logging
    # setup root logger
    setup_logging(loglevel='INFO', loggers=[''])

    with Connection('amqp://guest:guest@localhost:5672//') as conn:
        try:
            worker = Worker(conn)
            worker.run()
        except KeyboardInterrupt:
            print('bye bye')
