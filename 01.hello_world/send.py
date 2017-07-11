#!/usr/bin/env python
# coding=utf-8
# Author: zhuyuan

import pika
# 1.建立连接
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# 2.创建通道(channel)
channel = connection.channel()
# 3.创建queue,关于谁创建queue: Producer和Consumer都应该去创建。
channel.queue_declare(queue='hello')
# 4.发送消息
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
# 这里：1.exchange：指定exchange，这里使用默认的exchange
#       2.routing_key：指定queue的名字
#       3.body：消息内容
print " [x] Send 'Hello World!'"
# 5.关闭连接
connection.close()
