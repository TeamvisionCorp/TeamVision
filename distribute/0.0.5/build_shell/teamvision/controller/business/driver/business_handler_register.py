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
    def get_driver_instance(requestString):
        return BusinessDriverLoader.get_driver(requestString)
    
    @staticmethod
    def get_driver(requestString):
        handlerNames=BusinessDriverLoader.gethandlerfilename()
        for handlername in handlerNames:
            instance=BusinessDriverLoader.loadhandler(handlername,requestString)
            if instance.is_matched(requestString):
                break;
            else:
                instance=None
        return instance
                
    
    @staticmethod
    def loadhandler(handlerName,request_data):
        package= __import__(GlobalConfig.HANDLERPACKAGE+handlerName,fromlist=('agent','business','driver'))
        moudel=getattr(package,handlerName)
#         klass=getattr(moudel,handlerName)
        instance=moudel(request_data)
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