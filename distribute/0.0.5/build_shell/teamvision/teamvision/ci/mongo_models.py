#coding=utf-8
'''
Created on 2016-9-30

@author: zhangtiande
'''

from mongoengine import *
import datetime
from model_managers.mongo_model.mongo_model import MongoFile
from model_managers.mongo_model.mongo_model_manager import MongoFileManager
from teamvision.settings import MONGODB


connect(db=MONGODB['default']['DB'],alias=MONGODB['default']['ALIAS'], host=MONGODB['default']['HOST'], port=MONGODB['default']['PORT'])
class CIMongoModel(Document):
    meta={'abstract':True,'db_alias': MONGODB['default']['ALIAS']}
    is_active=BooleanField(default=True)
    create_time=DateTimeField(default=datetime.datetime.now())




class CITaskParameter(EmbeddedDocument):
    key = StringField(max_length=50)
    value =StringField(max_length=200)
    description=StringField(max_length=500,null=True)

class ParameterStepSettings(EmbeddedDocument):
    stage_id = StringField(max_length=100)
    step_id = StringField(max_length=100)
    is_on = BooleanField(default=False)
    step_order_index = IntField()
    step_name = StringField(max_length=30,null=True)
    stage_title = StringField(null=True)
    desc = StringField(max_length=200,null=True)

class CITaskParameterGroup(CIMongoModel):
    task_id = IntField(required=True)
    group_type=IntField(default=2)
    group_name=StringField(max_length=200,required=True)
    parameters =ListField(EmbeddedDocumentField(CITaskParameter),null=True)
    step_settings=ListField(EmbeddedDocumentField(ParameterStepSettings),null=True)
    description=StringField(max_length=500,null=True)
    is_default=BooleanField()


class CITaskStep(CIMongoModel):
    is_on = BooleanField(default=True)
    step_order_index = IntField()
    purpose_name = StringField(max_length=200,null=True)
    stage_id = StringField(required=True)
    step_config = DynamicField(null=True)
    # meta = {
    #     'abstract': True,
    # }

class CITaskStepPlugin(CIMongoModel):
    is_on = BooleanField(default=True)
    step_order_index = IntField()
    purpose_name = StringField(max_length=10,null=True)
    stage_id = StringField(required=True)


class CITaskSVNStep(CIMongoModel):
    step_name = StringField(max_length=30,default='SVN')
    step_id = IntField(default=1)
    repository_url = StringField(null=True)
    local_directory = StringField(null=True)
    user = StringField(null=True)
    password = StringField(null=True)
    checkout_stragegy = IntField(default=1)


class CITaskGitStep(CIMongoModel):
    step_name = StringField(max_length=30, default='GIT')
    step_id = IntField(default=2)
    repository_url = StringField(null=True)
    local_directory = StringField(null=True)
    branch = StringField(null=True)
    user = StringField(null=True)
    password = StringField(null=True)
    checkout_stragegy = IntField(default=1)



class CITaskCommandStep(CIMongoModel):
    step_name = StringField(max_length=30, default='命令行')
    step_id = IntField(default=3)
    command_line = StringField(null=True)
    upload_file_path = StringField(null=True)


class CITaskIOSStep(CIMongoModel):
    step_name = StringField(max_length=30, default='IOS构建')
    step_id = IntField(default=4)
    bundle_version = StringField(null=True)
    app_id = StringField(null=True)
    app_name = StringField(null=True)
    command_line = StringField(null=True)
    upload_file_path = StringField(null=True)



class CITaskAndroidStep(CIMongoModel):
    step_name = StringField(max_length=30, default='Android构建')
    step_id = IntField(default=5)
    command_line = StringField(null=True)
    upload_file_path = StringField(null=True)



class CITaskGATAPITestStep(CIMongoModel):
    step_name = StringField(max_length=30, default='GAT API 测试')
    step_id = IntField(default=6)
    autocase_filter = IntField()
    project_root_dir = StringField(null=True)
    upload_file_path = StringField(null=True)



class CITaskGATUITestStep(CIMongoModel):
    step_name = StringField(max_length=30, default='GAT UI 测试')
    step_id = IntField(default=7)
    autocase_filter = IntField()
    project_root_dir = StringField(null=True)
    upload_file_path = StringField(null=True)



class CITaskSSHStep(CIMongoModel):
    step_name = StringField(max_length=30, default='SSH远程服务')
    step_id = IntField(default=8)
    target_server = StringField(null=True)
    ssh_port = IntField(default=22)
    user = StringField(null=True)
    ssh_key = StringField(default="",null=True)
    password = StringField(null=True)
    source_file = StringField(null=True)
    exclude_file = StringField(null=True)
    target_dir = StringField(null=True)
    command_line = StringField(null=True)



class CITaskStage(CIMongoModel):
    task_id = IntField(required=True)
    stage_title = StringField(required=True)
    is_on = BooleanField(default=True)
    stage_order_index = IntField()


class CITaskAgentFilter(EmbeddedDocument):
    '''
    filter_type: 1 标签过滤，2 指定具体机器
    '''
    filter_type = IntField(default=1)
    agent_tags = ListField(IntField(),null=True)
    agent_id = IntField(null=True)

class CITaskTrigger(EmbeddedDocument):
    '''
    filter_type: 1 定时触发，2 SCM 触发
    '''
    trigger_type = IntField(default=1)
    schedule = StringField(null=True)
    scm = IntField(null=True)


class CITaskDefaultStage(CIMongoModel):
    task_id = IntField(required=True)
    stage_title= StringField(default='基本信息')
    stage_order_index = IntField(default=1)
    task_name = StringField(null=True)
    execute_strategy = IntField(default=1)
    agent_filter = EmbeddedDocumentField(CITaskAgentFilter)
    # task_trigger = EmbeddedDocumentField(CITaskTrigger)
    schedule = StringField(null=True)

