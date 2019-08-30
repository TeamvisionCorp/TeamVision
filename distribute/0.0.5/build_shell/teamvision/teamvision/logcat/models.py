#coding=utf-8
'''
Created on 2013-12-31

@author: ETHAN
'''

from django.db import models
from model_managers import logcat_model_manager



class LogCatModel(models.Model):
    CreationTime=models.DateTimeField(auto_now=True)
    IsActive=models.BooleanField(default=True)
    
    class Meta:
        abstract=True


class Logger(LogCatModel):
    deviceName=models.CharField(max_length=255,null=True)
    regTime=models.DateTimeField(auto_now=True)
    deviceId=models.CharField(max_length=50)
    extra=models.CharField(max_length=255,null=True)
    logFiles=models.CharField(max_length=50,null=True)
    appId=models.IntegerField()
    userAgent=models.CharField(max_length=255,null=True)
    objects=logcat_model_manager.LoggerManager()
    
    class Meta:
        app_label="logcat"
        db_table="logcat_logger"

    