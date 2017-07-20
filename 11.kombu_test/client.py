#!/usr/bin/env python
# coding=utf-8
# Author: zhuyuan

from __future__ import absolute_import, unicode_literals
from kombu import Connection
from kombu.pools import producers
from public import task_exchange, hello_task

priority_to_routing_key = {'high': 'hipri', 'mid': 'midpri', 'low': 'lopri'}


def send_as_task(conn, fun, args=(), kwargs={}, pri='low'):
    payload = {"fun": fun, "args": args, "kwargs": kwargs}
    routing_key = priority_to_routing_key[pri]

    with producers[conn].acquire(block=True) as producer:
        producer.publish(payload, exchange=task_exchange, serializer='pickle', compression='bzip2',declare=[task_exchange], routing_key=routing_key)


if __name__ == '__main__':
    conn = Connection('amqp://guest:guest@localhost:5672//')
    send_as_task(conn, fun=hello_task, args=('Kombu', 'low message'), kwargs={}, pri='low')
    send_as_task(conn, fun=hello_task, args=('Kombu', 'mid message'), kwargs={}, pri='mid')
    send_as_task(conn, fun=hello_task, args=('Kombu', 'high message'), kwargs={}, pri='high')
