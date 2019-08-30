#coding=utf-8
# coding=utf-8
'''
Created on 2014.1.15

@author: zhangtiande
'''

import os
from  agent.globalconfig import GlobalConfig

class BusinessDriverLoader(object):
    '''
    动态获取请求处理器
    '''
    @staticmethod
    def get_driver_instance(controller_message):
        return BusinessDriverLoader.get_driver(controller_message)
    
    @staticmethod
    def get_driver(controller_message):
        handlerNames=BusinessDriverLoader.gethandlerfilename()
        for handlername in handlerNames:
            instance=BusinessDriverLoader.loadhandler(handlername,controller_message)
            if instance.is_matched(controller_message.driver_key):
                break;
            else:
                instance=None
        return instance
                
    
    @staticmethod
    def loadhandler(handlerName,controller_message):
        package= __import__(GlobalConfig.HANDLERPACKAGE+handlerName,fromlist=('agent','business','driver'))
        moudel=getattr(package,handlerName)
#         klass=getattr(moudel,handlerName)
        instance=moudel(controller_message)
        return instance
    
    @staticmethod
    def gethandlerfilename():
        result=list()
        handlerNames=os.listdir(GlobalConfig.get_handler_package_path())
        for name in handlerNames:
            tempName=str(name.strip(".py"))
            if tempName.endswith("driver"):
                result.append(tempName)
        return result