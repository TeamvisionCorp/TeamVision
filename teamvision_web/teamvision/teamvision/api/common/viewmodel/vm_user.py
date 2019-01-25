#coding=utf-8
'''
Created on 2015-6-10

@author: zhangtiande
'''
from json.encoder import JSONEncoder

class VM_User(object):


    def __init__(self,user):
        '''
        Constructor
        '''
        self.user=user
    
    def get_user(self):
        result=dict()
        if self.user:
            result['code']=0
            result['username']=self.user.last_name+self.user.first_name
            result['email']=self.user.email
            result['message']="successful"
        else:
            result['code']=1
            result['username']=""
            result['email']=""
            result['message']="no user found"
        json_encoder=JSONEncoder() 
        return json_encoder.encode(result)
        
        