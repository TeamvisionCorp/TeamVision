#coding=utf-8
'''
Created on 2013-12-31

@author: ETHAN
'''
from django.db import models
from model_managers import interface_model_manager



class InterfaceModel(models.Model):
    CreationTime=models.DateTimeField(auto_now=True)
    IsActive=models.BooleanField(default=True)
    
    class Meta:
        abstract=True


class MockAPI(InterfaceModel):
    ApiTitle = models.CharField(max_length=50)
    ApiType = models.IntegerField()
    ApiPath = models.CharField(max_length=1000)
    HttpMethod = models.IntegerField(null=True)
    MockHandler = models.IntegerField()
    MockResponse = models.IntegerField()
    MockServer = models.IntegerField()
    MatchParten = models.CharField(max_length=20)
    Enable = models.BooleanField()
    Parent = models.IntegerField(default=0)
    Description = models.CharField(max_length=200,null=True,blank=True)
    objects = interface_model_manager.MockAPIManager()
    
    class Meta:
        app_label="interface"
        db_table="interface_mock_api"



class MockHandler(InterfaceModel):
    HandlerName = models.CharField(max_length=100)
    HandlerFile = models.CharField(max_length=100)
    HandlerFileName = models.CharField(max_length=100)
    Description = models.CharField(max_length=200,null=True)
    objects = interface_model_manager.MockHandlerManager()
    class Meta:
        app_label="interface"
        db_table="interface_mock_handler"


class MockResponse(InterfaceModel):
    ApiID = models.IntegerField()
    CallBackUrl = models.CharField(max_length=500,null=True,blank=True)
    CallBackMethod = models.IntegerField(default=1)
    Response = models.TextField()
    Enable = models.BooleanField(default=False)
    Description = models.CharField(max_length=200,null=True)
    objects = interface_model_manager.MockResponseManager()

    class Meta:
        app_label = "interface"
        db_table = "interface_mock_response"

    