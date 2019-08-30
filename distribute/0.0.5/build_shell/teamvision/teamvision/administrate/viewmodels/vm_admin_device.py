#coding=utf-8
'''
Created on 2015-11-4

@author: zhangtiande
'''

from business.administrate.device_service import DeviceService
from business.auth_user.user_service import UserService
from business.ucenter.account_service import AccountService
from business.common.system_config_service import SystemConfigService

import datetime



class VM_AdminDevice(object):
    '''
    classdocs
    '''
    
    def __init__(self,dm_device,is_create=False):
        self.is_create=is_create
        self.device=dm_device
    
    def device_os(self):
        result="fa-lightbulb-o"
        if self.device.DeviceOS==1:
            result="fa-android"
            
        if self.device.DeviceOS==2:
            result="fa-apple"
        
        if self.device.DeviceOS==3:
            result="fa-windows"
        return result
    
    def device_os_version(self):
        result="--"
        if self.device.DeviceOS!=0:
            result=SystemConfigService.get_device_version_name(self.device.DeviceOS,self.device.DeviceOSVersion)
        return result
    
    def device_screen(self):
        result="--"
        if self.device.DeviceScreenSize!=0:
            result=SystemConfigService.get_device_screen_size(self.device.DeviceScreenSize)
        return result
    
    def device_status(self):
        return SystemConfigService.get_device_status(self.device.DeviceStatus)
    
    def is_borrowed(self):
        result=False
        if self.device.DeviceStatus==2:
            result=True
        return result
    
    
    def is_ready(self):
        return DeviceService.is_ready(self.device)
    
    def is_ordered(self):
        return DeviceService.is_ordered(self.device)
        
            
    def borrower_avatar(self):
        result="/static/global/images/fruit-avatar/Fruit-1.png"
        if self.device.DeviceBorrower:
            borrower=UserService.get_user(self.device.DeviceBorrower)
            result=AccountService.get_avatar_url(borrower)
        return result
    
    def borrow_time(self):
        result=None
        if not self.device.DeviceBorrorwTime:
            result=self.device.DeviceBorrorwTime
        return result
    
    def borrower_name(self):
        result="--"
        if self.device.DeviceBorrower:
            borrower=UserService.get_user(self.device.DeviceBorrower)
            result=borrower.username
            if borrower:
                if borrower.first_name and borrower.last_name:
                    result=borrower.last_name+borrower.first_name
        return result
    
    def device_avatar(self):
        if self.device.DeviceOS==1:
            result="/static/global/images/device/device_android.png"
            
        if self.device.DeviceOS==2:
            result="/static/global/images/device/device_ios.png"
        
        if self.device.DeviceOS==0:
            result="/static/global/images/device/device-cellcard.jpg"   
        
        return result
        
    
    
    def form_action(self):
        if self.is_create:
            return "/administrate/device/create_post"
        else:
            return "/administrate/device/edit_post"
    
    
    
    
    
            
        
            
    
        