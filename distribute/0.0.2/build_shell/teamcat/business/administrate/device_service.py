#coding=utf-8
'''
Created on 2015-11-17

@author: zhangtiande
'''
from doraemon.administrate.models   import Device,DeviceManagementHistory
from django.contrib.admin.models import DELETION,CHANGE,ADDITION
from gatesidelib.datetimehelper import DateTimeHelper
from gatesidelib.common.simplelogger import SimpleLogger
import datetime


class DeviceService(object):
    '''
    classdocs
    '''
    
    
    @staticmethod
    def get_device(device_filter):
        result=None
        try:
            if device_filter.upper()=="ALL":
                result= Device.objects.all()
        
            if device_filter.upper()=="LENDING":
                result= Device.objects.lending_device()
        
            if device_filter.upper()=="ANDROID":
                result= Device.objects.android_device()
            
            if device_filter.upper()=="WP":
                result= Device.objects.wp_device()
        
            if device_filter.upper()=="IOS":
                result= Device.objects.ios_device()
        
            if device_filter.upper()=="OTHER":
                result= Device.objects.other()
        except Exception as ex:
            print(ex)
        return result
        
    @staticmethod
    def all_devices():
        return Device.objects.all()
        

    @staticmethod
    def get_device_byid(device_id):
        device=None
        try:
            device=Device.objects.get(device_id)
        except Exception as ex:
            print(ex)
        return device
                                                                               
    
    @staticmethod
    def create_device_post(request):
        new_device=Device()
        new_device=DeviceService.init_device(request, new_device)
        new_device.DeviceStatus=1
        new_device.IsActive=1
        new_device.save()
        DeviceService.log_create_activity(request.user,new_device)
    
    @staticmethod
    def edit_device_post(request):
        new_device=Device.objects.get(request.POST.get('device_id'))
        new_device=DeviceService.init_device(request, new_device)
        new_device.save()
        DeviceService.log_change_activity(request.user,new_device)
        
        
    @staticmethod    
    def delete_device(request):
        device_id=request.POST.get("device_id",0)
        device=Device.objects.get(device_id)
        device.IsActive=0
        device.save()
        DeviceService.log_delete_activity(request.user,device)
        
    @staticmethod    
    def borrow_device(request):
        message=""
        device_id=request.POST.get("device_id",0)
        device=Device.objects.get(device_id)
        if DeviceService.is_ready(device):
            device.DeviceStatus=3
            device.DeviceBorrorwTime=DateTimeHelper.getcnow()
            device.DeviceBorrower=request.user.id
            device.save()
            DeviceService.log_borrow_activity(request.user,device)
        else:
            message="此设备已经被借走，请联系管理员或者设备使用人。"
        return message
    
    @staticmethod    
    def lend_device(request):
        device_id=request.POST.get("device_id",0)
        device=Device.objects.get(device_id)
        device.DeviceStatus=2
        device.save()
        DeviceService.log_lend_activity(request.user,device)
    
    
    @staticmethod    
    def return_device(request):
        device_id=request.POST.get("device_id",0)
        device=Device.objects.get(device_id)
        device.DeviceStatus=1
        device.DeviceReturnTime=DateTimeHelper.getcnow()
        DeviceService.add_device_history(device)
        DeviceService.log_return_activity(request.user,device)
        device.DeviceBorrower=0
        device.save()
        
    

    @staticmethod
    def add_device_history(device):
        new_history=DeviceManagementHistory()
        new_history.DeviceBorrorwTime=device.DeviceBorrorwTime
        new_history.DeviceBorrower=device.DeviceBorrower
        new_history.DeviceID=device.id
        new_history.DeviceReturnTime=device.DeviceReturnTime
        new_history.save()
        
            
    @staticmethod
    def init_device(request,device):
        new_device=device
        new_device.DeviceName=request.POST.get("DeviceName")
        new_device.DeviceNumber=request.POST.get("DeviceNumber")
        new_device.DeviceOS=request.POST.get("DeviceOS")
        new_device.DeviceOSVersion=request.POST.get("DeviceOSVersion")
        new_device.DeviceScreenSize=request.POST.get("DeviceScreenSize")
        new_device.DeviceType=request.POST.get("DeviceType")
        new_device.DeviceBorrower=request.POST.get("DeviceBorrower")
        if new_device.DeviceBorrower!=0:
            new_device.DeviceStatus=2
            device.DeviceBorrorwTime=DateTimeHelper.getcnow()
            DeviceService.log_lend_activity(request.user,device)  
        return new_device
    
    @staticmethod
    def is_ready(device):
        result=False
        if device.DeviceStatus==1:
            result=True
        if device.DeviceStatus==2:
            result=False
        if device.DeviceStatus==3:
            if DateTimeHelper.get_time_to_now(str(device.DeviceBorrorwTime),"%Y-%m-%d %H:%M:%S+00:00")<=1800+28800:
                result=False
            else:
                result=True
                device.DeviceBorrorwTime=None
                device.DeviceStatus=1
                device.DeviceBorrower=0
                device.save()
        return result
    
    @staticmethod
    def is_ordered(device):
        result=False
        if device.DeviceStatus==3:
            if DateTimeHelper.get_time_to_now(str(device.DeviceBorrorwTime),"%Y-%m-%d %H:%M:%S+00:00")<=1800+28800:
                result=True
            else:
                result=False
                device.DeviceBorrorwTime=None
                device.DeviceStatus=1
                device.DeviceBorrower=0
                device.save()
        return result
    
    
    
    
    
    @staticmethod
    def log_create_activity(user,target):
        Device.objects.log_action(user.id,target.id,target.DeviceName,ADDITION,"添加了新设备",-1)
    
    @staticmethod
    def log_change_activity(user,target):
        Device.objects.log_action(user.id,target.id,target.DeviceName,CHANGE,"修改了设备信息",-1)
    
    @staticmethod
    def log_delete_activity(user,target):
        Device.objects.log_action(user.id,target.id,target.DeviceName,DELETION,"删除了新设备",-1)
    
    @staticmethod
    def log_borrow_activity(user,target):
        Device.objects.log_action(target.DeviceBorrower,target.id,target.DeviceName,DELETION,"预约了新设备",-1)
    
    @staticmethod
    def log_lend_activity(user,target):
        Device.objects.log_action(target.DeviceBorrower,target.id,target.DeviceName,DELETION,"借走了设备",-1)
        
    @staticmethod
    def log_return_activity(user,target):
        Device.objects.log_action(target.DeviceBorrower,target.id,target.DeviceName,DELETION,"归还了设备",-1)
    
                                                                      
            
            
        
        
        