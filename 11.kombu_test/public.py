#!/usr/bin/env python
# coding=utf-8
# Author: zhuyuan

from __future__ import absolute_import, unicode_literals
from kombu import Exchange, Queue

task_exchange = Exchange("tasks_direct", type="direct")

task_queues = {
    "low": Queue('lopri', task_exchange, routing_key='lopri', auto_),
    "mid": Queue('midpri', task_exchange, routing_key='midpri'),
    "high": Queue('hipri', task_exchange, routing_key='hipri'),
}


def hello_task(who='world'):
    print('Hello {0}'.format(who))
