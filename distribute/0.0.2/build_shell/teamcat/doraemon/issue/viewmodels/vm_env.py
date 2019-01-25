#coding=utf-8
# coding=utf-8
'''
Created on 2014-2-16

@author: ETHAN
'''


from business.env.version_service import VersionService
from business.common.system_config_service import SystemConfigService
from business.auth_user.user_service import UserService
from doraemon.interface.models import Product

class VM_ENV(object):
    '''
    MyPlace business model
    '''
    
    def __init__(self,loginuser,is_create,env,selected_env):

        self.user=loginuser
        self.is_create=is_create
        self.env=env
        self.selected_env=selected_env
    
    
    def private(self):
        result="checked"
        return result
    
    def internal(self):
        result=""
        if self.env.PBVisiableLevel==2:
            result="checked"
        return result
    
    def public(self):
        result=""
        if self.env.PBVisiableLevel==3:
            result="checked"
        return result
    
    def is_edit(self):
        result=""
        if not self.is_create:
            result="readonly"
        return result
    
    def form_id(self):
        if self.is_create:
            return "env-create-form"
        else:
            return "env-edit-form"
    
    def platform_flag(self):
        result="fa-flag-o"
        if self.env.PBPlatform==1:
            result="fa-android"
        
        if self.env.PBPlatform==2:
            result="fa-windows"
        
        if self.env.PBPlatform==3:
            result="fa-apple"
        if self.env.PBPlatform==4:
            result="fa-chrome"
        
        return result
    
    def platform_title(self):
        result=SystemConfigService.get_platform_name(self.env.PBPlatform)
        return result
    
    def lastest_version(self):
        result="--"
        version=VersionService.get_latest_version(self.env.id)
        if version:
            result=version.VVersion
        return result  
    
    def is_selected(self):
        if self.env.id==self.selected_env:
            return "selected"
    
    def env_creator(self):
        creator=UserService.get_user(self.env.PBCreator)
        result=creator.username
        if creator:
            if creator.first_name and creator.last_name:
                result=creator.last_name+creator.first_name
        return result
    
    def env_lead(self):
        lead=UserService.get_user(self.env.PBLead)
        result=lead.username
        if lead:
            if lead.first_name and lead.last_name:
                result=lead.last_name+lead.first_name
        return result
    
    def product_title(self):
        result="--"
        product=Product.objects.get(self.env.Product)
        if product:
            result=product.PTitle
        return result
    
    def has_module(self):
        if self.env.PBPlatform  in (4,6,7):
            return True
        else:
            return False
            
            
        
            
        
        
            
        
        
        