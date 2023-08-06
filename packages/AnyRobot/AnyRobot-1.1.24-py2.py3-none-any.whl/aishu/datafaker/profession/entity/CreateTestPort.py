
# !/usr/bin/env python
# -*- coding: UTF-8 -*-
from aishu.datafaker.profession.entity import port
from aishu.datafaker.profession.entity import ip
import requests
import time

class Port(object):
    def __init__(self):
        pass

    def httpport(self):
        url = 'http://{ip}/etl/input'.format(ip=ip.date().getTestHostIP)
        http_port = port.date().getEtlPortNew
        body = {
            "community":[],
            "port":http_port,
            "agentProtocol":"HTTP",
            "protocol":"AR-Agent",
            "ruleName":None,
            "status":1,
            "type":None,
            "tagsID":[],
            "tags":[],
            "timezone":"Asia/Shanghai",
            "charset":"UTF-8"
        }
        requests.post(url=url, json= body)
        time.sleep(1)
        print(http_port)
        return http_port

    def syslogPort(self):
        url_syslog = 'http://{ip}/etl/input'.format(ip=ip.date().getTestHostIP)
        syslog_port = port.date().getEtlPortNew
        body_syslog = {
            "community":[],
            "port": syslog_port,
            "protocol":"syslog",
            "ruleName":None,
            "status":1,
            "tagsID":[],
            "tags":[],
            "timezone":"Asia/Shanghai",
            "type":"syslog",
            "charset":"UTF-8"
        }
        requests.post(url=url_syslog, json= body_syslog)
        time.sleep(60)
        print(syslog_port)
        return syslog_port

