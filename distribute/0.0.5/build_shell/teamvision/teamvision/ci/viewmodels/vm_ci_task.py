#coding=utf-8
'''
Created on 2015-11-4

@author: Devuser
'''
from django.shortcuts import HttpResponse
from teamvision.project.models import Project,Tag
from teamvision.ci.models import CITaskHistory
from business.ci.ci_task_parameter_service import CITaskParameterService
from business.ci.ci_task_history_service import CITaskHistoryService

from teamvision.ci.viewmodels.vm_ci_task_config import VM_CITaskConfig

class VM_CITask(object):
    '''
    classdocs
    '''
    
    def __init__(self,dm_ci_task,tag_menu,show_tag,is_full_part,parameter_group_menu=None):
        self.ci_task=dm_ci_task
        self.tag_menu=tag_menu
        self.parameter_group_menu=parameter_group_menu
        self.show_tag=show_tag
        self.task_config=VM_CITaskConfig(self.ci_task.TaskConfig)
        self.is_full_part=is_full_part
        self.product_id=Project.objects.get(self.ci_task.Project).Product
    
    def task_type_name(self):
        result="deploy"
        if self.ci_task.TaskType==4:
            result="build"
        
        if self.ci_task.TaskType==5:
            result="deploy"
        
        if self.ci_task.TaskType==1:
            result="testing"
        return result
    
    def task_type_label(self):
        result="D"
        if self.ci_task.TaskType==4:
            result="B"
        
        if self.ci_task.TaskType==5:
            result="D"
        
        if self.ci_task.TaskType==1:
            result="T"
        return result
        
    
    def last_run_time(self):
        result="从未运行过"
        last_history=CITaskHistoryService.get_finished_history(self.ci_task.id)
        if len(last_history):
            result=last_history[0].CreateTime
        return result
        
    def is_task_success(self):
        result=".status-background-fail"
        if self.task.TStatus==1:
            result=".status-background-success"
        if self.task.TStatus==2:
            result=".status-background-fail"
        if self.task.TStatus==3:
            result=".status-background-cancel"
        return result
        
    def task_project_title(self):
        return Project.objects.get(self.ci_task.Project).PBTitle
    
    def task_project_avatar(self):
        return Project.objects.get(self.ci_task.Project).PBAvatar
    
    def has_parameters(self):
        return CITaskParameterService.has_parameters(self.ci_task.id)
    
    def last_build_success(self):
        result="status-background-default"
        last_history=CITaskHistoryService.get_finished_history(self.ci_task.id)
        if len(last_history):
            if last_history[0].BuildStatus==1:
                result="status-background-success"
            if last_history[0].BuildStatus==2:
                result="status-background-fail"
            if last_history[0].BuildStatus==3:
                result="status-background-cancel"
        return result
            
    
    def task_tags(self):
        result=list()
        if self.ci_task.Tags:
            for tag_id in eval(self.ci_task.Tags):
                tmp_tag=Tag.objects.get(tag_id)
                if tmp_tag:
                    result.append(tmp_tag)              
        return result
    
    def is_test_task(self):
        result=""
        if self.ci_task.TaskType==1:
            result='checked'
        return result
    
    def is_build_task(self):
        result=""
        if self.ci_task.TaskType==4:
            result='checked'
        return result
    
    def is_deploy_task(self):
        result=""
        if self.ci_task.TaskType==5:
            result='checked'
        return result
    def task_history_url(self):
        if self.ci_task.TaskType==4:
            result="/ci/build/"+str(self.ci_task.id)+"/history"
        if self.ci_task.TaskType==5:
            result="/ci/deploy/"+str(self.ci_task.id)+"/history"
        if self.ci_task.TaskType==1:
            result="/ci/testing/"+str(self.ci_task.id)+"/history"
        return result