#coding=utf-8
'''
Created on 2015-11-17

@author: zhangtiande
'''
from doraemon.project.models import ProjectRole

class VM_MemberRole(object):
    '''
    classdocs
    '''


    def __init__(self,role,member_role_id,login_user):
        '''
        Constructor
        '''
        self.login_user=login_user
        self.role=role
        self.member_role_id=member_role_id
    
    
    def member_role(self):
        result=""
        if self.role.id==self.member_role_id:
            result="fa-check"
        else:
            result=""
        return result
        
    
            
        
        