#coding=utf-8
'''
Created on 2015-10-22

@author: zhangtiande
'''

from gatesidelib.common.simplelogger import SimpleLogger
from model_managers.model_manager import ModelManager


class MockAPIManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):
        
        return super(MockAPIManager,self).get_queryset().filter(IsActive=1)
    
    def get(self,api_id):
        result=None
        try:
            result=super(MockAPIManager,self).get_queryset().get(id=api_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

    def get_children(self,parent_id):
        result=list()
        try:
            result=self.all().filter(Parent=parent_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

class MockHandlerManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):

        return super(MockHandlerManager,self).get_queryset().filter(IsActive=1)

    def get(self,handler_id):
        result=None
        try:
            result=super(MockHandlerManager,self).get_queryset().get(id=handler_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

class MockResponseManager(ModelManager):
    '''
    classdocs
    '''
    def all(self):

        return super(MockResponseManager,self).get_queryset().filter(IsActive=1)

    def get(self,response_id):
        result=None
        try:
            result=super(MockResponseManager,self).get_queryset().get(id=response_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result

    def get_responses(self,api_id):
        result=None
        try:
            result=super(MockResponseManager,self).get_queryset().get(ApiID=api_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result