#coding=utf-8
# coding=utf-8
'''
Created on 2014-2-16

@author: ETHAN
'''

# from dataaccess.common.dal_dictvalue import DAL_DictValue
# from business.common.userservice import UserService
# from dataaccess.testjob.dal_testjob import DAL_TestJob
import time
import datetime
from business.project.version_service import VersionService
from business.common.system_config_service import SystemConfigService
from business.auth_user.user_service import UserService
from teamvision.project.models import Product

class VM_Project(object):
    '''
    MyPlace business model
    '''
    
    def __init__(self,loginuser,is_create,project,selected_project):

        self.user=loginuser
        self.is_create=is_create
        self.project=project
        self.selected_project=selected_project
    
    
    def private(self):
        result="checked"
        return result
    
    def internal(self):
        result=""
        if self.project.PBVisiableLevel==2:
            result="checked"
        return result
    
    def public(self):
        result=""
        if self.project.PBVisiableLevel==3:
            result="checked"
        return result
    
    def is_edit(self):
        result=""
        if not self.is_create:
            result="readonly"
        return result
    
    def form_id(self):
        if self.is_create:
            return "project-create-form"
        else:
            return "project-edit-form"
    
    def platform_flag(self):
        result="fa-flag-o"
        if self.project.PBPlatform==1:
            result="fa-android"
        
        if self.project.PBPlatform==2:
            result="fa-windows"
        
        if self.project.PBPlatform==3:
            result="fa-apple"
        if self.project.PBPlatform==4:
            result="fa-chrome"
        
        return result
    
    def platform_title(self):
        result=SystemConfigService.get_platform_name(self.project.PBPlatform)
        return result
    
    def lastest_version(self):
        result="--"
        version=VersionService.get_latest_version(self.project.id)
        if version:
            result=version.VVersion
        return result  
    
    def is_selected(self):
        if str(self.project.id)==str(self.selected_project):
            return "selected"
        else:
            return ""
    
    def project_creator(self):
        creator=UserService.get_user(self.project.PBCreator)
        result=creator.username
        if creator:
            if creator.first_name and creator.last_name:
                result=creator.last_name+creator.first_name
        return result
    
    def project_lead(self):
        lead=UserService.get_user(self.project.PBLead)
        result=lead.username
        if lead:
            if lead.first_name and lead.last_name:
                result=lead.last_name+lead.first_name
        return result
    
    def product_title(self):
        result="--"
        product=Product.objects.get(self.project.Product)
        if product:
            result=product.PTitle
        return result
    
    def has_module(self):
        if self.project.PBPlatform  in (4,6,7):
            return True
        else:
            return False
            
            
        
            
        
        
            
        
        
        