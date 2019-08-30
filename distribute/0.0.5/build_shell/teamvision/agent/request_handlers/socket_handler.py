#coding=utf-8
# coding=utf-8
'''
Created on 2014.1.15

@author: zhangtiande
'''

import socketserver
from gatesidelib.common.simplelogger import SimpleLogger
from agent.business.driver.business_driver_loader import BusinessDriverLoader
from agent.request_handlers.driver_pool import DriverPool
from agent.socket_message.controller_pb2 import Controller,TQCommand
from agent.socket_message.agent_pb2 import Agent,TaskResult
import time



class SocketHandler(socketserver.StreamRequestHandler):
    
    def handle(self):
        '''
        socket server 处理接收到的请求。
                            首先读取请求内容，然后查找匹配的处理器，最后调用处理发送返回值
        '''
        SimpleLogger.info("in socket handler")
        controller_message=self.reciveRequest()
        self.send_return_value(controller_message)
        self.process_request(controller_message)
        SimpleLogger.info("finised socket process")
    
    def reciveRequest(self):
        '''
                         获取请求内容
        '''
        SimpleLogger.info("start recive data from controller")
        controller_message=None
        try:
            data=self.rfile.read1(1024)
            controller_message=Controller()
            controller_message.ParseFromString(data)
            SimpleLogger.info("recive job from controller. the job uuid  is:["+str(controller_message.task_uuid)+"]")
        except Exception as ex:
            SimpleLogger.info("recive data from controller fail and error message is:"+str(ex))
            SimpleLogger.error(ex)
        return controller_message
            
    
    def send_return_value(self,controller_message):
        '''
                         发送返回值
        '''
        SimpleLogger.info("start send return value to  controller")
        try:
            agent_message=Agent()
            agent_message.task_id=controller_message.task_id
            agent_message.task_uuid=controller_message.task_uuid
            agent_message.result=TaskResult.Value("SUCCESS")
            agent_message.message="recive task successfully!"
            if controller_message==None:
                agent_message.task_result=TaskResult.Value("FAIL")
                agent_message.message="recive task fail!"
            return_value=agent_message.SerializeToString()      
            self.wfile.write(return_value)
        except Exception as ex:
            SimpleLogger.info("send value to controller fail and error message is:"+str(ex))
            SimpleLogger.error(ex)
            
    
    def process_request(self,controller_message):
        SimpleLogger.info("Start processing job. the job uuid  is:["+controller_message.task_uuid+"]")
        try:
            self.start(controller_message)
            self.stop(controller_message)
        except Exception as ex:
            SimpleLogger.info("Process job fail  the job uuid  is:["+controller_message.task_uuid+"]")
            SimpleLogger.info("Error:"+str(ex))
            SimpleLogger.error(ex)
    
    def start(self,controller_message):
        driver_pool=DriverPool()
        if controller_message.task_command!=TQCommand.Value("START"):
            return
        else:
            SimpleLogger.info("Start job, the job uuid  is:["+controller_message.task_uuid+"]")
            if not driver_pool.has_value(controller_message.task_uuid):
                request_driver=BusinessDriverLoader.get_driver_instance(controller_message)
                if request_driver:
                    request_driver.start()
                    driver_pool.put_value(controller_message.task_uuid,request_driver)
                else:
                    raise Exception("can not find driver with driver key "+controller_message.driver_key)
            else:
                raise Exception("the job with uuid "+controller_message.task_uuid+"is running!")
            
    def stop(self,controller_message):
        driver_pool=DriverPool()
        if controller_message.task_command!=TQCommand.Value("STOP"):
            return
        else:
            SimpleLogger.info("Stop job, the job uuid  is:["+controller_message.task_uuid+"]")
            if driver_pool.has_value(controller_message.task_uuid):
                driver_pool.get_value(controller_message.task_uuid).stop()
                driver_pool.clear(controller_message.task_uuid)
            else:
                raise Exception("no running job found  with uuid "+controller_message.task_uuid)
                
            
            
            
            
    
    
          
        
        
        