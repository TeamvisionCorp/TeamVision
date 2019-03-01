#coding=utf-8
'''
Created on 2016-7-6

@author: Administrator
'''

from teamvision.project.models import Tag

class VM_CICredential(object):
    '''
    classdocs
    '''


    def __init__(self,dm_credential,is_create,selected_credential_id):
        '''
        Constructor
        '''
        self.ci_credential=dm_credential
        self.selected_credential_id=selected_credential_id
        self.is_create=is_create
    
    def every_one(self):
        result=""
        if self.ci_credential.Scope==None or self.ci_credential.Scope==1:
            result="checked"
        return result
    
    def only_me(self):
        result=""
        if self.ci_credential.Scope==2:
            result="checked"
        return result
    
    def Credential_type(self):
        result=""
        if self.ci_credential.CredentialType==1:
            result="fa-key"
            
        if self.ci_credential.CredentialType==2:
            result="fa-file"
        return result
    
    def scope_name(self):
        result=""
        if self.ci_credential.Scope==1:
            result="fa-unlock"
        
        if self.ci_credential.Scope==2:
            result="fa-lock"
        
        return result
    def is_selected(self):
        result=""
        if self.selected_credential_id:
            if self.ci_credential.id==int(self.selected_credential_id):
                result="selected"
        return result
        
        
        
                 
            
        
   
    
    
    
                
        