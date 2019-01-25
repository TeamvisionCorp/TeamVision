#coding=utf-8
'''
Created on 2013-12-31
 
@author: zhangtiande
'''
from django.conf import settings
 
from django.db import models
from model_managers import administrate_model_manager
from django.contrib.admin.models import ContentType
 
 
class Device(models.Model):
    DeviceNumber=models.CharField(max_length=10)
    DeviceName=models.CharField(max_length=100)
    DeviceOS=models.IntegerField()
    DeviceOSVersion=models.IntegerField()
    DeviceScreenSize=models.IntegerField()
    DeviceStatus=models.IntegerField()
    DeviceType=models.IntegerField()
    DeviceSerialNum=models.CharField(max_length=100,null=True)
    DeviceAvatar=models.IntegerField(default=0)
    DeviceBorrower=models.IntegerField(default=0)
    DeviceBorrorwTime=models.DateTimeField(null=True)
    DeviceReturnTime=models.DateTimeField(null=True)
    IsActive=models.BooleanField()
    objects=administrate_model_manager.DeviceManager()
    class Meta:
        app_label="administrate"
        db_table="device_management"
 
class DeviceManagementHistory(models.Model):
    DeviceID=models.IntegerField()
    DeviceBorrower=models.IntegerField()
    DeviceBorrorwTime=models.DateTimeField()
    DeviceReturnTime=models.DateTimeField()
    objects=administrate_model_manager.DeviceHistoryManager()
    class Meta:
        app_label="administrate"
        db_table="device_management_history"
     
