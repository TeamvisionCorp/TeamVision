#coding=utf-8
'''
Created on 2016-3-8

@author: Devuser
'''

from socket import *
import sys
  

class SocketClient(object):
    
    def __init__(self,host,port):
        self.host=host
        self.port=port
    
    def send_data(self,data,buffer_size):
        addr =(self.host,self.port)
        client = socket(AF_INET,SOCK_STREAM)  
        client.connect(addr)
        client.send(data.encode('utf-8'))
        data=client.recv(buffer_size).decode('utf-8')
        client.close()