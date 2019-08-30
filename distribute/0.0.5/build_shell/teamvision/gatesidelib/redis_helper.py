#coding=utf-8
'''
Created on 2016-9-13

@author: Devuser
'''
import redis

class RedisHelper(object):
    '''
    classdocs
    '''


    def __init__(self,host,port,db):
        '''
        Constructor
        '''
        self.host=host
        self.port=port
        self.db=db
        self.pool=redis.ConnectionPool(host=host,port=port,db=db)
    
    def set_value(self,key,value,ex):
        r=redis.Redis(connection_pool=self.pool)
        r.set(key,value,ex)
    
    def get_value(self,key):
        result=""
        r=redis.Redis(connection_pool=self.pool)
        if r.exists(key):
            result=r.get(key).decode('utf-8')
        return result
    
    def get_object(self,key):
        result=""
        r=redis.Redis(connection_pool=self.pool)
        if r.exists(key):
            result=r.get(key)
        return result
    
    def delete_value(self,key):
        result=""
        r=redis.Redis(connection_pool=self.pool)
        if r.exists(key):
            result=r.delete(key)
        return result
        
    def append(self,key,value,ex):
        r=redis.Redis(connection_pool=self.pool)
        if r.exists(key):
            r.append(key,value)
        else:
            r.set(key,value,ex)
    
    def set_svalue(self,key,values,max_ex):
        r=redis.Redis(connection_pool=self.pool)
        r.sadd(key,values)
        r.expire(key,max_ex)
    
    def srem_value(self,key,values):
        r=redis.Redis(connection_pool=self.pool)
        r.srem(key,values)
        
    def get_svalue(self,key):
        r=redis.Redis(connection_pool=self.pool)
        return r.smembers(key)
    
    def has_key(self,key):
        r=redis.Redis(connection_pool=self.pool)
        return r.exists(key)
    
    def publish(self,channel,message):
        r=redis.Redis(connection_pool=self.pool)
        return r.publish(channel, message)
        
        
        
        
    
        