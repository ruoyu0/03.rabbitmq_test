#!/usr/bin/env python
# coding=utf-8
# Author: zhuyuan

import time
from oslo_config import cfg
import oslo_messaging as messaging

CONF_PATH = "rpc.conf"

RPC_CONF = cfg.ConfigOpts()
RPC_CONF(["--config-file", CONF_PATH])


class HelloEndpoint(object):
    def hello(self, ctx, msg):
        print "call hello func!", "msg:", msg, "ctx:", ctx
        return "received"


class CalcFib(object):
    #  计算斐波那契数列
    def fib(self, ctx, n):
        print "call fib func"
        fib_func = lambda n: n if n<=2 else fib_func(n-1) + fib_func(n-2)
        return fib_func(n)


endpoints = [HelloEndpoint(), CalcFib()]

# 获取使用的消息通信介质
transport = messaging.get_transport(RPC_CONF)
# 生成需要匹配的目标
target = messaging.Target(topic="test_topic", server="server1")
# 生成server
server = messaging.get_rpc_server(transport, target, endpoints, executor='blocking')
# 开始监听
try:
    server.start()
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping server")

server.stop()
server.wait()
