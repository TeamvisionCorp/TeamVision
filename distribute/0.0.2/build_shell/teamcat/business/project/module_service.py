#coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''
from doraemon.project.models import Project,ProjectModule
from gatesidelib.common.simplelogger import SimpleLogger
from django.contrib.admin.models import DELETION,CHANGE,ADDITION

class ModuleService(object):
    '''
    classdocs
    '''
    

    @staticmethod
    def create_module(request,projectid):
        try:
            module=ProjectModule()
            module.ProjectID=projectid
            module.Name=request.POST.get('Name')
            module.IsActive=1
            module.save()
            print(module.id)
            ModuleService.log_create_activity(request.user, module)
        except Exception as ex:
            print(ex)
            SimpleLogger.error(ex)
    
    
    @staticmethod
    def delete_module(request,module_id):
        module=ProjectModule.objects.get(module_id)
        module.IsActive=0
        module.save()
        ModuleService.log_delete_activity(request.user, module)
    
    
    @staticmethod
    def update_module(module_id,field_name,value,user):
        module=ProjectModule.objects.get(module_id)
        module.__dict__[field_name]=value
        module.IsActive=1
        module.save()
        ModuleService.log_change_activity(user, module)
            
        
    
    
    @staticmethod
    def log_create_activity(user,target):
        ProjectModule.objects.log_action(user.id,target.id,target.Name,ADDITION,"创建了新模块",target.ProjectID)
    
    @staticmethod
    def log_delete_activity(user,target):
        ProjectModule.objects.log_action(user.id,target.id,target.Name,ADDITION,"删除了模块",target.ProjectID)
    
    @staticmethod
    def log_change_activity(user,target):
        ProjectModule.objects.log_action(user.id,target.id,target.Name,ADDITION,"修改了模块",target.ProjectID)
        
        