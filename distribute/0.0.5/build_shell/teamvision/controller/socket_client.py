#coding=utf-8
'''
Created on 2016-3-8

@author: zhangtiande
'''

from socket import *
import sys
from controller.socket_message.controller_pb2 import  TQTaskType,TQCommand,Controller
  

def send_data():
    host = 'localhost'  
    port = 8080  
    bufsize = 1024  
    while True:  
        data =sys.stdin.readline()
        if not data or data=='exit':  
            break

        controller=Controller()
        controller.task_id=1
        controller.task_type=TQTaskType.Value("AUTOTESTTASK")
        controller.task_uuid="123"
        if data.strip('\n')=="s":
            controller.task_command=TQCommand.Value("STOP")
        else:
            controller.task_command=TQCommand.Value("START")
        
        controller.driver_key="DRIVER_KEY"
        request_data=controller.SerializeToString()
        addr = (host,port)  
        client = socket(AF_INET,SOCK_STREAM)  
        client.connect(addr)
        client.send(request_data)  
        data=client.recv(bufsize).decode()
        print(data)
        client.close()
    



if __name__ == '__main__':
    send_data()