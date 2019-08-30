#coding=utf-8
'''
Created on 2015-5-14

@author: Devuser
'''
import httplib2
from urllib.parse import urlencode



class HttpLibHelper(object):
    '''
    classdocs
    '''
    @staticmethod
    def send_request(uri,httpmethod,parameters):
        conn = httplib2.Http(".cache")
        response,content=conn.request(uri,httpmethod,body=urlencode(parameters))
        return response,content
    
    
    def send_request_with_parameters(self,uri,httpmethod,parameters):
        conn = httplib2.Http(".cache")
        response,content=conn.request(uri, httpmethod,body=urlencode(parameters))
        return response,content
    
    def send_request_with_header(self,uri,httpmethod,parameters,headers):
        '''
        headers={'Cookie': response['set-cookie']}
        headers = {'Content-type': 'application/x-www-form-urlencoded'}  
        '''
        conn = httplib2.Http(".cache")
        response,content=conn.request(uri, httpmethod,body=urllib.urlencode(parameters),headers=headers)
        return response,content
    
    def send_request_with_password(self,uri,httpmethod,parameters,headers,name,password):
        conn = httplib2.Http(".cache")
        conn.add_credentials(name, password)
        response,content=conn.request(uri, httpmethod,body=urllib.urlencode(parameters),headers=headers)
        return response,content
    
    def send_request_with_cert(self,uri,httpmethod,parameters,headers,key,cert):
        conn = httplib2.Http(".cache")
        conn.add_certificate(key, cert)
        response,content=conn.request(uri, httpmethod,body=urllib.urlencode(parameters),headers=headers)
        return response,content