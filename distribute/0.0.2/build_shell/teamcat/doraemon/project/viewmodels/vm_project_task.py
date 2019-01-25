#coding=utf-8
'''
Created on 2015-11-4

@author: Devuser
'''
from django.shortcuts import HttpResponse
from doraemon.project.models import Project,Tag
from doraemon.project.viewmodels.vm_task_owner import VM_TaskOwner
from django.contrib.auth.models import User

class VM_ProjectTask(object):
    '''
    classdocs
    '''
    
    def __init__(self,dm_task,tag_menu,owner_menu, project_menu=None,is_create=True,page_fullpart=True,show_user=True,show_tag=True):
        self.tag_menu=tag_menu
        self.project_menu=project_menu
        self.owner_menu=owner_menu
        self.task=dm_task
        self.is_create=is_create
        self.is_fullpart=page_fullpart
        self.show_user=show_user
        self.show_tag=show_tag
        
    
    def is_task_finished(self):
        if self.task.Status==1:
            return "finished-check fa-check-square"
        else:
            return "fa-square-o unfinished-check"
    
    def task_title(self):
        if self.task.Status==1:
            return "<del>"+self.task.Title+"</del>"
        else:
            return self.task.Title
        
    def task_project_title(self):
        return Project.objects.get(self.task.ProjectID).PBTitle
    
    def task_project_avatar(self):
        return Project.objects.get(self.task.ProjectID).PBAvatar
    
    def task_tags(self):
        result=list()
        if self.task.Tags:
            for tag_id in eval(self.task.Tags):
                tmp_tag=Tag.objects.get(tag_id)
                if tmp_tag:
                    result.append(tmp_tag)              
        return result
    
    def task_owners(self):
        owners=list()
        if self.task.Owner:
            if self.task.Owner.endswith(','):
                for ownerid in eval(self.task.Owner):
                    tmp_user=User.objects.get(id=ownerid)
                    owners.append(VM_TaskOwner(self.task,tmp_user,None))
            else:
                tmp_user=User.objects.get(id=self.task.Owner)
                owners.append(VM_TaskOwner(self.task,tmp_user,None))
        return owners