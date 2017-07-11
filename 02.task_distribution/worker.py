#!/usr/bin/env python
# coding=utf-8
# Author: zhuyuan

import time
import pika
# 1.建立连接
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
# 2.创建通道(channel)
channel = connection.channel()
# 3.创建queue,关于谁创建queue: Producer和Consumer都应该去创建。
channel.queue_declare(queue='hello')

# 4.定义回调函数
def callback(ch, method, properties, body):  
    print " [x] Received %r" % (body,)  
    time.sleep(body.count('.'))  
    print " [x] Done"  

# 5.订阅消息(subscribe)
channel.basic_consume(callback, queue='hello', no_ack=True)
# 这里：1.callback：处理接收到的数据的回调函数
#       2.queue：指定queue的名字
#       3.no_ack：不需要ack回应
print ' [*] Waiting for messages. To exit press CTRL+C'
# 6.开始无限循环监听
channel.start_consuming()
