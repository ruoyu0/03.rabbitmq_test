#!/usr/bin/env python
# coding=utf-8
# Author: zhuyuan

from oslo_config import cfg
import oslo_messaging as messaging

CONF_PATH = "rpc.conf"

RPC_CONF = cfg.ConfigOpts()
RPC_CONF(["--config-file", CONF_PATH])


class RpcClient(object):
    def __init__(self, rpc_conf, topic):
        # 获取使用的消息通信介质
        transport = messaging.get_transport(rpc_conf)
        # 生成需要匹配的目标
        target = messaging.Target(topic=topic, version='1.0', fanout=False)
        # 创建连接客户端
        self._client = messaging.RPCClient(transport, target)

    def call(self, method, *args, **kwargs):
        # 发起请求，去调用远程方法
        context_dict = {"a":"ctx_msg"}
        result = self._client.call(context_dict, method, **kwargs)
        # context_dict: 上下文，oslo.messaging会将该dict传递给远程方法的ctx参数
        # call_method：请求的方法
        # arg： 请求的参数
        return result


rpc_client = RpcClient(RPC_CONF, topic="test_topic")
# 调用远程方法，测试
print "result:", rpc_client.call(method="hello", msg="hello server!")
# 调用远程方法，计算斐波那契数
print "result:", rpc_client.call(method="fib", n=23)
