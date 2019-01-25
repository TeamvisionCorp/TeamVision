#coding=utf-8
'''
Created on 2015-9-24

@author: zhangtiande
'''
from doraemon.administrate.pagefactory.administrate_pageworker import AdminPageWorker
from doraemon.administrate.viewmodels.admin_left_nav_bar import AdminPermissionLeftNavBar
from doraemon.administrate.viewmodels.admin_sub_nav_bar import AdminPermissionSubNavBar
from doraemon.administrate.pagefactory.admin_template_path import AdminPermissionPath,AdminCommonPath
from doraemon.administrate.viewmodels.vm_admin_permission import VM_AdminPermission
from business.auth_user.permission_service import PermissionService
from business.common.system_config_service import SystemConfigService
from django.contrib.auth.models import User
import random

class AdminPermissionPageWorker(AdminPageWorker):
    '''
    项目页面生成器
    '''
    
    def __init__(self,request):
        '''
        Constructor
        '''
        AdminPageWorker.__init__(self, request)
        self.left_nav_bar_model=AdminPermissionLeftNavBar
        self.subpage_model=AdminPermissionSubNavBar
    
    def get_admin_permission_page(self,request,sub_nav_action):
        sub_leftnav=self.get_permission_sub_navbar(request,sub_nav_action)
        left_nav_bar=self.get_admin_left_bar(request,sub_nav_action)
        admin_permission_webpart=self.get_permission_list_webpart()
        pagefileds={'left_nav_bar':left_nav_bar,'sub_nav_bar':sub_leftnav,"admin_permission_webpart":admin_permission_webpart}
        return self.get_page(pagefileds,AdminPermissionPath.admin_permission_index,request)
    
    def get_admin_left_bar(self,request,sub_nav_action):
        return self.get_left_nav_bar(request,self.left_nav_bar_model,AdminPermissionPath.admin_permission_left_nav,sub_nav_action=sub_nav_action)
    
    def get_permission_sub_navbar(self,request,sub_nav_action):
        permissions_count=len(PermissionService.all_custom_permissions())
        return self.get_sub_nav_bar(request, self.subpage_model,AdminPermissionPath.admin_permission_subnav,sub_nav_action=sub_nav_action,permissions_count=permissions_count)
    
    def get_permission_list_webpart(self):
        permissions=PermissionService.all_custom_permissions()
        permission_list_controll=self.get_permission_list_controll(permissions)
        pagefileds={"permission_list_controll":permission_list_controll,"permissions":permissions}
        return self.get_webpart(pagefileds,AdminPermissionPath.admin_permission_list_webpart)
    

    
    def get_permission_list_controll(self,permissions):
        vm_permissions=list()
        for permission in permissions:
            tmp_permission=VM_AdminPermission(permission,0)
            vm_permissions.append(tmp_permission)
        pagefileds={"permissions":vm_permissions}
        return self.get_webpart(pagefileds, AdminPermissionPath.admin_permission_list_control)
    
    def get_permission_create_dialog(self,request):
        tmp_permission=VM_AdminPermission(None,0,is_create=True)
        content_type_control=self.get_content_type_controll()
        permission_form=self.get_webpart({"permission":tmp_permission,"content_type_control":content_type_control},AdminPermissionPath.admin_permission_form)
        return self.get_page({"formhtml":permission_form},AdminPermissionPath.admin_permission_create_dialog,request)
    
    
    def get_content_type_controll(self):
        permission_types=SystemConfigService.get_permission_types()
        pagefileds={"permission_types":permission_types}
        return self.get_webpart(pagefileds,AdminCommonPath.content_type_dropdownlist)
            
        
        
        
    
  
    