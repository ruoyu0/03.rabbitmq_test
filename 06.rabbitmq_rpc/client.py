#!/usr/bin/env python
# coding=utf-8
# Author: zhuyuan

#!/usr/bin/env python
import pika
import uuid


class FibonacciRpcClient(object):
    def __init__(self):
        # 建立连接，然后建立通道channel
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

        # 创建queue，名称随机，这里用于接收server返回的消息
        result = self.channel.queue_declare(exclusive=True)
        # 获取queue的名称
        self.callback_queue = result.method.queue
        # 开始监听，等待server返回结果 
        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        # 生成uuid，这里用于生成唯一值
        self.corr_id = str(uuid.uuid4())
        # 发送消息
        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            # 为了收到响应，这里需要提供一个”callback“（回调）的queue地址
            properties=pika.BasicProperties(reply_to=self.callback_queue, correlation_id=self.corr_id,),
            # reply_to: 一般用来指明用于回调的queue（Commonly used to name a callback queue）
            # correlation_id: 在请求中关联处理RPC响应（correlate RPC responses with requests）
            body=str(n)
        )
        while self.response is None:
            self.connection.process_data_events()
        return int(self.response)


fibonacci_rpc = FibonacciRpcClient()

print " [x] Requesting fib(30)"
response = fibonacci_rpc.call(30)
print " [.] Got %r" % (response,)
