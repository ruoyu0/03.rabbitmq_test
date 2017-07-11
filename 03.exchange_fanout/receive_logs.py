#!/usr/bin/env python
# coding=utf-8
# Author: zhuyuan

import time
import pika

# 1.建立连接
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# 2.创建通道(channel)
channel = connection.channel()
channel.exchange_declare(exchange="logs", type="fanout")
# 创建一个新的queue，名字让rabbitmq随机生成
result = channel.queue_declare(exclusive=True)
# 取得queue的名字
queue_name = result.method.queue
# 将新生成的queue和exchange绑定 
channel.queue_bind(exchange='logs', queue=queue_name)

# 4.定义回调函数
def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)

# 5.订阅消息(subscribe)
channel.basic_consume(callback, queue=queue_name, no_ack=True)
# 这里：1.callback：处理接收到的数据的回调函数
#       2.queue：指定queue的名字
#       3.no_ack：不需要ack回应
print ' [*] Waiting for messages. To exit press CTRL+C'
# 6.开始无限循环监听
channel.start_consuming()
