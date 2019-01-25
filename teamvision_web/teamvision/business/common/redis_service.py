#coding=utf-8
'''
Created on 2016-10-25

@author: zhangtiande
'''
from gatesidelib.redis_helper import RedisHelper
from business.business_service import BusinessService
from teamvision.settings import REDIS
import  pickle
from ws4redis.redis_store import RedisMessage
from ws4redis.publisher import RedisPublisher

class RedisService(BusinessService):
    '''
    classdocs
    '''
    HOST=REDIS['default']['HOST']
    PORT=REDIS['default']['PORT']
    DB=REDIS['default']['DB']
    EXPIRE=REDIS['default']['EXPIRE']
    
    @staticmethod
    def set_object(key,obj,ex=None):
        redis_helper=RedisHelper(RedisService.HOST,RedisService.PORT,RedisService.DB)
        if ex==None:
            ex=RedisService.EXPIRE
        redis_helper.set_value(key,pickle.dumps(obj), ex)
    
    @staticmethod
    def get_object(key):
        result=None
        redis_helper=RedisHelper(RedisService.HOST,RedisService.PORT,RedisService.DB)
        if redis_helper.get_object(key):
            object_byte=redis_helper.get_object(key)
            result=pickle.loads(object_byte)
        return result
    
    
    
    @staticmethod
    def set_value(key,value,ex=None):
        redis_helper=RedisHelper(RedisService.HOST,RedisService.PORT,RedisService.DB)
        if ex==None:
            ex=RedisService.EXPIRE
        redis_helper.set_value(key, value, ex)
    
    @staticmethod
    def get_value(key):
        result=""
        redis_helper=RedisHelper(RedisService.HOST,RedisService.PORT,RedisService.DB)
        if redis_helper.get_value(key):
            result=redis_helper.get_value(key)
        return result
    
    @staticmethod
    def set_svalue(key,values,ex=None):
        redis_helper=RedisHelper(RedisService.HOST,RedisService.PORT,RedisService.DB)
        if ex==None:
            ex=RedisService.EXPIRE
        redis_helper.set_svalue(key, values, ex)
    
    @staticmethod
    def get_svalue(key):
        redis_helper=RedisHelper(RedisService.HOST,RedisService.PORT,RedisService.DB)
        set_value=redis_helper.get_svalue(key)
        result=set()
        for item in set_value:
            temp=item.decode("utf-8")
            result.add(temp)
        return result
    
    @staticmethod
    def delete_smember(key,values):
        redis_helper=RedisHelper(RedisService.HOST,RedisService.PORT,RedisService.DB)
        result=redis_helper.srem_value(key, values)
        
    
    @staticmethod
    def append_value(key,value,ex):
        redis_helper=RedisHelper(RedisService.HOST,RedisService.PORT,RedisService.DB)
        if ex==None:
            ex=RedisService.EXPIRE
        redis_helper.append(key, value,ex)
    
    @staticmethod
    def delete_value(key):
        redis_helper=RedisHelper(RedisService.HOST,RedisService.PORT,RedisService.DB)
        redis_helper.delete_value(key)
        
    @staticmethod
    def has_key(key):
        redis_helper=RedisHelper(RedisService.HOST,RedisService.PORT,RedisService.DB)
        return redis_helper.has_key(key)
    
    @staticmethod
    def publish_message(channel,message):
        redis_helper=RedisHelper(RedisService.HOST,RedisService.PORT,RedisService.DB)
        return redis_helper.publish(channel, message)

    @staticmethod
    def websocket_publish_message(channel,message):
        websocket_message = RedisMessage(message)  # create a welcome message to be sent to everybody
        RedisPublisher(facility=channel, broadcast=True).publish_message(websocket_message)
        
    
        
        