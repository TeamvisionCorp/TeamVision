#coding=utf-8
'''
Created on 2014-12-17

@author: Devuser
'''
import memcache

class MemcachHelper(object):
    '''
    classdocs
    '''
    
    def __init__(self,serverurl,serverport):
        self.url=serverurl
        self.port=serverport
        print([self.url+":"+self.port])
    
    def get_value(self,key):
        mc = memcache.Client([self.url+":"+self.port], debug=1)
        print(key)
        print(mc.get(key.encode('utf-8')))
        return mc.get(str(key))
    
    def set_value(self,key,value):
        mc = memcache.Client([self.url+':'+self.port], debug=0)
        mc.set(str(key),str(value))
        
    def set_value_expire(self,key,value,expire):
        mc = memcache.Client([self.url+':'+self.port], debug=0)
        mc.set(str(key),str(value),expire)
    
    def delete(self,key,time):
        mc = memcache.Client([self.url+':'+self.port], debug=0)
        mc.delete(str(key),time)
        
