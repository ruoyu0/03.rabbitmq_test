#!/usr/bin/env python
# coding=utf-8
# Author: zhuyuan

import sys
from oslo_config import cfg

# 默认组的配置项
service_opts = [
    cfg.StrOpt('username', default='default', help='user name'),
    cfg.StrOpt('password', help='password')
]

# 自定义配置组
rabbit_group = cfg.OptGroup(name='rabbit', title='RabbitMQ options')

# 配置组中的多配置项模式
rabbit_Opts = [
    cfg.StrOpt('host', default='localhost', help='IP/hostname to listen on.'),
    cfg.IntOpt('port', default=5672, help='Port number to listen on.')
]


CONF = cfg.CONF
# 注册默认组的配置项
CONF.register_opts(service_opts)
# 配置组必须在其组件被注册前注册！
CONF.register_group(rabbit_group)
# 注册配置组中含有多个配置项的模式，必须指明配置组
CONF.register_opts(rabbit_Opts, rabbit_group)


# 设置默认的配置文件名
CONF(sys.argv[1:], default_config_files=['app.conf'])

# 使用配置项，print
print ("username=%s" % (CONF.username))
print ("rabbitmq.host=%s rabbitmq.port=%s" % (CONF.rabbit.host, CONF.rabbit.port))
