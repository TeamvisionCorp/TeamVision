#coding=utf-8
'''
Created on 2016-9-30

@author: zhangtiande
'''

from mongoengine import *
import datetime
from model_managers.mongo_model.mongo_model import MongoFile
from model_managers.mongo_model.mongo_model_manager import MongoFileManager
from doraemon.settings import MONGODB


connect(db=MONGODB['default']['DB'],alias=MONGODB['default']['ALIAS'], host=MONGODB['default']['HOST'], port=MONGODB['default']['PORT'])
#connect('doraemon', host=MONGO_HOST, port=MONGO_HOST_PORT)
class CIMongoModel(Document):
    meta={'abstract':True,'db_alias': MONGODB['default']['ALIAS']}
    is_active=BooleanField(default=True)
    create_time=DateTimeField(default=datetime.datetime.now())



class ReplaceFileMap(EmbeddedDocument):
    file_id = IntField(required=True)
    file_name = StringField(max_length=270)
    replace_targets =StringField(max_length=500)

class DeployServiceReplaceConfig(CIMongoModel):
    service_id = IntField(required=True)
    replace_target_map =ListField(EmbeddedDocumentField(ReplaceFileMap))



class CITaskParameter(EmbeddedDocument):
    key = StringField(max_length=50)
    value =StringField(max_length=200)
    description=StringField(max_length=500)

class CITaskParameterGroup(CIMongoModel):
    task_id = IntField(required=True)
    group_type=IntField(default=2)
    group_name=StringField(max_length=200,required=True)
    parameters =ListField(EmbeddedDocumentField(CITaskParameter),null=True)
    step_plugin_is_enable=ListField(StringField(max_length=200))
    enable_plugin_settings=BooleanField(default=False)
    description=StringField(max_length=500,null=True)
    is_default=BooleanField(default=False)


class CIServiceMongoFile(MongoFile):
    DB=MONGODB['default']['DB']
    PORT=MONGODB['default']['PORT']
    HOST=MONGODB['default']['HOST']
    objects=MongoFileManager(HOST,PORT,DB,"ci_service")
    



    