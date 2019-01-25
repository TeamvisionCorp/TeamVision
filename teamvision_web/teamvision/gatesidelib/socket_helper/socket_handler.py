#coding=utf-8
# coding=utf-8
'''
Created on 2014.1.15

@author: zhangtiande
'''

import socketserver
from gatesidelib.common.simplelogger import SimpleLogger
import time



class SocketHandler(socketserver.StreamRequestHandler):
    
    def handle(self):
        '''
        socket server 处理接收到的请求。
                            首先读取请求内容，然后查找匹配的处理器，最后调用处理发送返回值以及执行回到接口
        '''
        request_data=self.reciveRequest()
        self.send_return_value(request_data)
    
    def reciveRequest(self):
        '''
                         获取请求内容
        '''
        data=self.rfile.read1(1024).decode('UTF-8')
        return data
    
    def send_return_value(self,return_data):
        '''
                         发送返回值
        '''
        self.wfile.write(return_data.encode("utf-8"))
        