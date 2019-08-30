#coding=utf-8
'''
Created on 2015-9-24

@author: zhangtiande
'''
from teamvision.administrate.pagefactory.administrate_pageworker import AdminPageWorker
from teamvision.administrate.viewmodels.admin_left_nav_bar import AdminSystemRoleLeftNavBar
from teamvision.administrate.viewmodels.admin_sub_nav_bar import AdminSystemRoleSubNavBar
from teamvision.administrate.pagefactory.admin_template_path import AdminSystemRolePath
from teamvision.administrate.pagefactory.admin_permission_pageworker import AdminPermissionPageWorker
from teamvision.administrate.viewmodels.vm_admin_system_role import VM_SystemRole
from teamvision.administrate.viewmodels.vm_admin_permission import VM_AdminPermission
from business.auth_user.permission_service import PermissionService
from business.auth_user.system_role_service import SystemRoleService
from django.contrib.auth.models import User
import random

class AdminSystemRolePageWorker(AdminPageWorker):
    '''
    项目页面生成器
    '''
    
    def __init__(self,request):
        '''
        Constructor
        '''
        AdminPageWorker.__init__(self, request)
        self.left_nav_bar_model=AdminSystemRoleLeftNavBar
        self.subpage_model=AdminSystemRoleSubNavBar
    
    def get_admin_system_role_page(self,request,sub_nav_action):
        sub_leftnav=self.get_system_role_sub_navbar(request,sub_nav_action)
        left_nav_bar=self.get_admin_left_bar(request,sub_nav_action)
        admin_system_role_webpart=self.get_system_role_list_webpart()
        pagefileds={'left_nav_bar':left_nav_bar,'sub_nav_bar':sub_leftnav,"admin_system_role_webpart":admin_system_role_webpart}
        return self.get_page(pagefileds,AdminSystemRolePath.admin_system_role_index,request)
    
    def get_admin_system_role_edit_page(self,request,roleid,sub_nav_action):
        sub_leftnav=self.get_system_role_sub_navbar(request,sub_nav_action)
        left_nav_bar=self.get_admin_left_bar(request,sub_nav_action)
        admin_system_role_edit_webpart=self.get_role_permission_edit_webpart(roleid)
        pagefileds={'left_nav_bar':left_nav_bar,'sub_nav_bar':sub_leftnav,"admin_system_role_edit_webpart":admin_system_role_edit_webpart}
        return self.get_page(pagefileds,AdminSystemRolePath.admin_system_role_index,request)
    
    def get_admin_left_bar(self,request,sub_nav_action):
        return self.get_left_nav_bar(request,self.left_nav_bar_model,AdminSystemRolePath.admin_system_role_left_nav,sub_nav_action=sub_nav_action)
    
    def get_system_role_sub_navbar(self,request,sub_nav_action):
        system_role_count=len(SystemRoleService.all_roles())
        return self.get_sub_nav_bar(request, self.subpage_model,AdminSystemRolePath.admin_system_role_subnav,sub_nav_action=sub_nav_action,system_role_counts=system_role_count)
    
    def get_system_role_list_webpart(self):
        roles=SystemRoleService.all_roles()
        system_role_list_controll=self.get_system_role_list_controll(roles)
        pagefileds={"system_role_list_controll":system_role_list_controll,"roles":roles}
        return self.get_webpart(pagefileds,AdminSystemRolePath.admin_system_role_list_webpart)
    
    def get_role_permission_edit_webpart(self,roleid):
        role=SystemRoleService.get_role(roleid)
        temp_role=VM_SystemRole(role)
        all_custom_permissions=PermissionService.all_custom_permissions()
        permission_list_webpart=self.get_role_permission_controll(all_custom_permissions,roleid)
        pagefileds={"role":temp_role,'permission_list_webpart':permission_list_webpart}
        return self.get_webpart(pagefileds,AdminSystemRolePath.admin_system_role_edit_page)
    
    def get_role_permission_controll(self,permissions,roleid):
        vm_permissions=list()
        for permission in permissions:
            tmp_permission=VM_AdminPermission(permission,roleid)
            vm_permissions.append(tmp_permission)
        pagefileds={"permissions":vm_permissions}
        return self.get_webpart(pagefileds,AdminSystemRolePath.admin_system_role_permission_list) 
        
    
    def get_system_role_list_controll(self,roles):
        vm_roles=list()
        for role in roles:
            tmp_role=VM_SystemRole(role)
            vm_roles.append(tmp_role)
        pagefileds={"roles":vm_roles}
        return self.get_webpart(pagefileds, AdminSystemRolePath.admin_system_role_list_control)
    
        
        
        
    
  
    