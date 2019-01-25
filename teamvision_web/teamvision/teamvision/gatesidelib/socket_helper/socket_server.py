#coding=utf-8
# coding=utf-8
'''
Created on 2014.1.15

@author: zhangtiande
'''

import os
import sys
import threading
from socketserver import ThreadingTCPServer



class SocketServer(object):
    
    @staticmethod       
    def get_default_server(host,port,socket_handler):
        '''
           实例化 socket server
        '''
        server = ThreadingTCPServer((host,port),socket_handler)
        return server

    @staticmethod
    def start_server(server):
        '''
           以多线程方式，正式启动socket server
        '''
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.setDaemon(True)
        server_thread.start()
        server.serve_forever()

    @staticmethod
    def shutdown_server(server):
        server.shutdown()

