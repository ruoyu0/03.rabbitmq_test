#!/usr/bin/env python
# coding=utf-8
# Author: zhuyuan

import pika
# 用户处理client请求，并回应


def fib(n):
    return n if n in [0, 1] else fib(n - 1) + fib(n - 2)


# 建立连接和通道
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
# 创建queue
channel.queue_declare(queue='rpc_queue')

# 定义回调函数
def on_request(ch, method, props, body):
    n = int(body)
    print " [.] fib(%s)" % (n,)
    response = fib(n)
    # 处理完函数后，发送消息给rabbitmq
    ch.basic_publish(
        exchange='',
        #routing_key
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=str(response)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


# 设置同一个时间点最多处理一个Message
channel.basic_qos(prefetch_count=1)
# 定义消息
channel.basic_consume(on_request, queue='rpc_queue')

print " [x] Awaiting RPC requests"
# 开始监听
channel.start_consuming()
