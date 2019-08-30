#coding=utf-8
'''
Created on 2016-8-24

@author: Devuser
'''

from json.encoder import JSONEncoder

class Response(object):
    '''
    API 接口简单返回值
    '''
    
    def __init__(self):
        pass
    
    def get_json(self):
        json_encoder=JSONEncoder()
        result=json_encoder.encode(self.__dict__)
        return result
            


class SuccessResponse(Response):
    '''
    API 接口简单返回值
    '''
    
    def __init__(self,message,result):
        self.code=0
        self.msg=message
        self.result=result

class ErrorResponse(Response):
    '''
    API 接口简单返回值
    '''
    
    def __init__(self,message,result):
        self.code=1001
        self.msg=message
        self.result=result
        