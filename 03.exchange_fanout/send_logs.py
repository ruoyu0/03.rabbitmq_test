#!/usr/bin/env python
# coding=utf-8
# Author: zhuyuan

import sys
import pika

# 1.建立连接
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# 2.创建通道(channel)
channel = connection.channel()
# 3.创建exchange
channel.exchange_declare(exchange="logs", type="fanout")

# 4.发送消息
message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs', routing_key='', body=message)
print " [x] Sent %r" % (message,)  
# 5.关闭连接
connection.close()
