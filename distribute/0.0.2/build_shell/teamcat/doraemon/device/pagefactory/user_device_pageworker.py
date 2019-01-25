#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from doraemon.device.pagefactory.pageworker import DevicePageWorker
from doraemon.home.viewmodels.home_left_nav_bar import HomeDeviceLeftNavBar
from doraemon.device.pagefactory.device_template_path import DevicePagePath
from doraemon.administrate.viewmodels.vm_admin_device import VM_AdminDevice

from business.administrate.device_service import DeviceService
# from business.project.project_service import ProjectService

class UserDevicePageWorker(DevicePageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self,request):
        '''
        Constructor
        '''
        DevicePageWorker.__init__(self, request)
        self.pagemodel=HomeDeviceLeftNavBar
        
    
    def get_device_fullpage(self,request):
        left_nav_bar=self.get_device_left_bar(request)
        device_list=self.get_device_list_page(request)
        pagefileds={'left_nav_bar':"","device_list":device_list}
        return self.get_page(pagefileds,DevicePagePath.device_page_path,request)
    
    def get_device_left_bar(self,request):
        return self.get_left_nav_bar(request,self.pagemodel,DevicePagePath.left_nav_template_path)
    
    
    def get_device_list_page(self,request):
        pagefileds={}
        return self.get_webpart(pagefileds,DevicePagePath.device_list_page)
    
    def get_device_list_controll(self,request):
        device_filter=request.POST.get("device_filter")
        dm_devices=DeviceService.get_device(device_filter)
        vm_devices=list()
        for device in dm_devices:
            tmp_device=VM_AdminDevice(device,0)
            vm_devices.append(tmp_device)
        pagefileds={"devices":vm_devices}
        web_part=self.get_webpart(pagefileds,DevicePagePath.device_list_controll)
        return web_part
    
        
        