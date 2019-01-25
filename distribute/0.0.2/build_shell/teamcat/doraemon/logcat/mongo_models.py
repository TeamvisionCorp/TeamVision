#coding=utf-8
'''
Created on 2016-9-30

@author: Administrator
'''

from mongoengine import *
import datetime
from doraemon.settings import MONGODB
from model_managers.logcat_model_manager import BusinessLogManager

connect(db=MONGODB['log']['DB'],alias=MONGODB['log']['ALIAS'],port=MONGODB['log']['PORT'],host=MONGODB['log']['HOST'])

class LogCatMongoModel(Document):
    meta={'abstract':True,'db_alias':MONGODB['log']['ALIAS']}
    is_active=BooleanField(default=True)
    create_time=DateTimeField(default=datetime.datetime.now())


class BusinessLog(LogCatMongoModel):
    appId = IntField(required=True)
    eventId =StringField(required=True)
    userId =IntField()
    channel =IntField(required=True)
    model =StringField(max_length=50,required=True)
    os =StringField(max_length=50,required=True)
    data =StringField(max_length=500,required=True)
    deviceId =StringField(max_length=50,required=True)
    appVersion =StringField(max_length=20,required=True)
    buildVersion=StringField(max_length=20)
    isThird=BooleanField()
    timestamp=StringField(max_length=50)
    



    