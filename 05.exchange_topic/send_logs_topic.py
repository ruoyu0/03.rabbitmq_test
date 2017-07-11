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
channel.exchange_declare(exchange="topic_logs", type="topic")

# 4.发送消息
severity = sys.argv[1] if len(sys.argv) > 1 else "anonymous.info"
message = ' '.join(sys.argv[2:]) or "Hello World!"
channel.basic_publish(exchange='topic_logs', routing_key=severity, body=message)
print " [x] Sent %r:%r" % (severity, message,)  
# 5.关闭连接
connection.close()
