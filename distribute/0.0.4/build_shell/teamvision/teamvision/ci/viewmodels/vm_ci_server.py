#coding=utf-8
'''
Created on 2016-7-6

@author: Administrator
'''

from teamvision.project.models import Tag

class VM_CIServer(object):
    '''
    classdocs
    '''


    def __init__(self,dm_server,is_create,selected_server_id):
        '''
        Constructor
        '''
        self.ci_server=dm_server
        self.selected_server_id=selected_server_id
        self.is_create=is_create
        
    def is_selected(self):
        result=""
        if self.ci_server.id==int(self.selected_server_id):
            result="selected"
        return result
    
    def every_one(self):
        result=""
        if self.ci_server.Scope==None or self.ci_server.Scope==1:
            result="checked"
        return result
    
    def only_me(self):
        result=""
        if self.ci_server.Scope==2:
            result="checked"
        return result
    
    
    def scope_name(self):
        result=""
        if self.ci_server.Scope==1:
            result="所有人可以使用"
        
        if self.ci_server.Scope==2:
            result="仅自己可以使用"
        
        return result
        
        
        
                 
            
        
   
    
    
    
                
        