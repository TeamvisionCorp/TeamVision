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
        self.pool=redis.ConnectionPool(host=host,port=port)
    
    def set_value(self,key,value,ex):
        r=redis.Redis(connection_pool=self.pool)
        r.set(key,value,ex)
    
    def get_value(self,key):
        result=""
        r=redis.Redis(connection_pool=self.pool)
        if r.exists(key):
            result=r.get(key).decode('utf-8')
        return result
        
    def append(self,key,value,ex):
        r=redis.Redis(connection_pool=self.pool)
        if r.exists(key):
            r.append(key,value)
        else:
            r.set(key,value,ex)
        