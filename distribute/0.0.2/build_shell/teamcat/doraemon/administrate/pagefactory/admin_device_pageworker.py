#coding=utf-8
'''
Created on 2015-9-24

@author: zhangtiande
'''
from doraemon.administrate.pagefactory.administrate_pageworker import AdminPageWorker
from doraemon.administrate.viewmodels.admin_left_nav_bar import AdminDeviceLeftNavBar
from doraemon.administrate.viewmodels.admin_sub_nav_bar import AdminDeviceSubNavBar
from doraemon.administrate.pagefactory.admin_template_path import AdminDevicePath,AdminCommonPath
from doraemon.administrate.viewmodels.vm_admin_device import VM_AdminDevice
from doraemon.administrate.viewmodels.vm_device_dropdownlist_controll import VM_DropDownControll
from doraemon.administrate.models import Device
from business.administrate.device_service import DeviceService
from business.common.system_config_service import SystemConfigService
from doraemon.auth_extend.user.pagefactory.user_common_pageworker import UserCommonControllPageWorker
import random

class AdminDevicePageWorker(AdminPageWorker):
    '''
    项目页面生成器
    '''
    
    def __init__(self,request):
        '''
        Constructor
        '''
        AdminPageWorker.__init__(self, request)
        self.left_nav_bar_model=AdminDeviceLeftNavBar
        self.subpage_model=AdminDeviceSubNavBar
    
    def get_admin_device_page(self,request,sub_nav_action):
        admin_device_webpart=self.get_device_list_webpart(request,sub_nav_action)
        return self.generate_admin_device_page(request, sub_nav_action, admin_device_webpart)
    
    def get_device_create_page(self,request,device_id):
        admin_device_webpart=self.get_device_create_webpart(request,device_id)
        return self.generate_admin_device_page(request,"all", admin_device_webpart)
    
    
    def get_admin_left_bar(self,request,sub_nav_action):
        return self.get_left_nav_bar(request,self.left_nav_bar_model,AdminDevicePath.admin_device_left_nav,sub_nav_action=sub_nav_action)
    
    def get_device_sub_navbar(self,request,sub_nav_action):
        return self.get_sub_nav_bar(request, self.subpage_model,AdminDevicePath.admin_device_subnav,sub_nav_action=sub_nav_action)
    
    def get_device_list_webpart(self,request,device_filter):
        devices=DeviceService.get_device(device_filter)
        device_list_controll=self.get_device_list_controll(devices)
        pagefileds={"device_list_controll":device_list_controll,"devices":devices,"webpart_title":self.get_device_webpart_title(device_filter)}
        return self.get_webpart(pagefileds,AdminDevicePath.admin_device_list_webpart)
    
    
    def get_device_webpart_title(self,device_filter):
        result=None
        if device_filter.upper()=="ALL":
            result="所有设备  "
        
        if device_filter.upper()=="LENDING":
            result="出借设备  "
        
        if device_filter.upper()=="ANDROID":
            result="Android设备  "
        
        if device_filter.upper()=="IOS":
            result="IOS设备  "
        
        if device_filter.upper()=="OTHER":
            result="其他设备  "
        
        return result
        
    def get_device_list_controll(self,devices):
        vm_devices=list()
        for device in devices:
            tmp_device=VM_AdminDevice(device,0)
            vm_devices.append(tmp_device)
        pagefileds={"devices":vm_devices}
        return self.get_webpart(pagefileds, AdminDevicePath.admin_device_list_control)
    
    def get_device_create_webpart(self,request,device_id):
        if device_id==0:
            dm_device=Device()
            tmp_device=VM_AdminDevice(None,is_create=True)
        else:
            dm_device=DeviceService.get_device_byid(device_id)
            tmp_device=VM_AdminDevice(dm_device,is_create=False)
        user_common_page_worker=UserCommonControllPageWorker(request)
        device_os_controll=self.get_device_os_controll(dm_device)
        device_os_version_controll=self.get_device_os_version_controll(dm_device)
        device_screen_controll=self.get_screen_size_controll(dm_device)
        device_type_controll=self.get_device_type_controll(dm_device)
        device_borrower_controll=user_common_page_worker.get_user_dropdown_list(dm_device.DeviceBorrower)
        page_fileds={"device_type_controll":device_type_controll,"device":tmp_device,"device_os_controll":device_os_controll,"device_os_version_controll":device_os_version_controll,"device_screen_controll":device_screen_controll}
        page_fileds["device_borrower_controll"]=device_borrower_controll
        device_form=self.get_webpart(page_fileds,AdminDevicePath.admin_device_form)
        device_form_create_webpart=self.get_webpart({"device_create_form":device_form},AdminDevicePath.admin_device_create_page)
        return device_form_create_webpart
    
    def get_device_borrow_dialog(self,request):
        device_id=request.POST.get("device_id")
        device=Device.objects.get(device_id)
        vm_device=VM_AdminDevice(device,False)
        pagefileds={"device":vm_device}
        return self.get_webpart(pagefileds, AdminDevicePath.admin_device_borrow_confirm_dialog)
    
    def generate_admin_device_page(self,request,sub_nav_action,webpart):
        sub_leftnav=self.get_device_sub_navbar(request,sub_nav_action)
        left_nav_bar=self.get_admin_left_bar(request,sub_nav_action)
        pagefileds={'left_nav_bar':left_nav_bar,'sub_nav_bar':sub_leftnav,"admin_device_webpart":webpart}
        return self.get_page(pagefileds,AdminDevicePath.admin_device_index,request)
    
    def get_device_os_controll(self,dm_device):
        device_os=SystemConfigService.get_device_os()
        return self.get_device_dropdown_controll(device_os,dm_device.DeviceOS)
    
    def get_device_os_version_controll(self,dm_device,os_value=1):
        select_value=0
        if dm_device !=None:
            os_value=dm_device.DeviceOS
            select_value=dm_device.DeviceOSVersion
        
        device_os_version=SystemConfigService.get_device_os_version(os_value)
        if device_os_version==None:
            return ""
        return self.get_device_dropdown_controll(device_os_version,select_value)
    
    def get_screen_size_controll(self,dm_device):
        screen_size=SystemConfigService.get_screen_szie()
        return self.get_device_dropdown_controll(screen_size,dm_device.DeviceScreenSize)
    
    def get_device_type_controll(self,dm_device):
        device_type=SystemConfigService.get_device_type()
        return self.get_device_dropdown_controll(device_type,dm_device.DeviceType)
    
    
    def get_device_dropdown_controll(self,dic_datas,selected_value):
        vm_controlls=self.get_common_controll_vms(dic_datas,selected_value)
        pagefileds={"dic_datas":vm_controlls}
        return self.get_webpart(pagefileds,AdminCommonPath.dicdata_dropdownlist)
    
    
    def get_common_controll_vms(self,dm_list,selected_value):
        result=list()
        for os in dm_list:
            result.append(VM_DropDownControll(os,selected_value))
        return result
        
        
            
        
        
        
    
  
    