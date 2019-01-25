#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from json.encoder import JSONEncoder

class Response(object):
    '''
    API 接口简单返回值
    '''
    
    def __init__(self,status,message):
        self.status=status
        self.message=message
    
    def get_json(self):
        json_encoder=JSONEncoder()
        result=json_encoder.encode(str(self.__dict__))
        return result

class ResUploadPackage(Response):
    '''
    Upload package API 接口简单返回值
    '''
    
    def __init__(self,status,message,file_id):
        Response.__init__(ResUploadPackage, status, message)
        self.file_id=file_id

        