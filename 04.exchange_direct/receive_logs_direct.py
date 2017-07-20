#!/usr/bin/env python
# coding=utf-8
# Author: zhuyuan

import sys
import pika

# 1.建立连接
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# 2.创建通道(channel)
channel = connection.channel()
channel.exchange_declare(exchange="direct_logs", type="direct")
# 创建一个新的queue，名字让rabbitmq随机生成，并让连接关闭时删除该queue
result = channel.queue_declare(exclusive=True)
# 取得queue的名字
queue_name = result.method.queue

# 获取severities
severities = sys.argv[1:]
if not severities:
    print >> sys.stderr, "Usage: %s [info] [warning] [error]" % (sys.argv[0],)  
    sys.exit(1)

# 将新生成的queue和exchange绑定
for severity in severities: 
    channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)

# 4.定义回调函数
def callback(ch, method, properties, body):
    print " [x] %r:%r" % (method.routing_key, body,) 

# 5.订阅消息(subscribe)
channel.basic_consume(callback, queue=queue_name, no_ack=True)
# 这里：1.callback：处理接收到的数据的回调函数
#       2.queue：指定queue的名字
#       3.no_ack：不需要ack回应
print ' [*] Waiting for messages log level: [%s]. To exit press CTRL+C' % " ".join(severities)
# 6.开始无限循环监听
channel.start_consuming()
