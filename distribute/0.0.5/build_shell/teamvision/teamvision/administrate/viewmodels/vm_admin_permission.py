#coding=utf-8
'''
Created on 2015-11-4

@author: zhangtiande
'''

from business.auth_user.permission_service import PermissionService
from business.auth_user.system_role_service import SystemRoleService
from business.common.system_config_service import SystemConfigService



class VM_AdminPermission(object):
    '''
    classdocs
    '''
    
    def __init__(self,row,role_id,is_create=False):
        if row:
            self.id=row[0]
            self.name=row[1]
            self.description=row[2]
            self.permission_type=self.set_permission_type(row[3])
        self.is_create=is_create
        self.role_id=role_id
        
    
    def set_permission_type(self,permission_type):
        return SystemConfigService.get_permission_type(permission_type)
    
    def is_permission_active(self):
        result=""
        if self.role_id:
            role=SystemRoleService.get_role(self.role_id)
            permission=PermissionService.get_permission(self.id)
            if permission in role.permissions.all():
                result="active"
        return result
            
        
            
    
        