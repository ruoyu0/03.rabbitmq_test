#!/usr/bin/env python
# coding=utf-8
# Author: zhuyuan

import sys
import pika

message = ' '.join(sys.argv[1:]) or "Hello World!"

# 1.建立连接
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# 2.创建通道(channel)
channel = connection.channel()
# 3.创建queue,关于谁创建queue: Producer和Consumer都应该去创建。
channel.queue_declare(queue='hello')
# 4.发送消息
channel.basic_publish(exchange='', routing_key='hello', body=message)
# 5.关闭连接
connection.close()
