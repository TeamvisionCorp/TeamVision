#coding=utf-8
'''
Created on 2014-12-17

@author: zhangtiande
'''

from gatesidelib.memcache.memcachhelper import MemcachHelper

class MemcacheService(object):
    '''
    classdocs
    '''

    @staticmethod
    def get_value(request):
        key=request.GET['key']
        serverurl=request.GET['server']
        serverport=request.GET['port']
        isemail=request.GET['isemail']
        if isemail=='True':
            key="EmailCaptche:"+key
        else:
            key="PhoneCaptche:"+key
        print(key)
        memHelper=MemcachHelper(serverurl,serverport)
        return memHelper.get_value(key)
    
    @staticmethod
    def set_value(request):
        key=request.GET['key']
        value=request.GET['value']
        serverurl=request.GET['server']
        serverport=request.GET['port']
        isemail=request.GET['isemail']
        if isemail=='True':
            key="EmailCaptche:"+key
        else:
            key="PhoneCaptche:"+key
        memHelper=MemcachHelper(serverurl,serverport)
        memHelper.set_value(key, value)
    