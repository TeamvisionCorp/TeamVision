#coding=utf-8
'''
Created on 2015-11-17

@author: zhangtiande
'''
from teamvision.project.models import ProjectMember
from django.contrib.auth.models import User
from business.ucenter.account_service import AccountService


class VM_TaskOwner(object):
    '''
    classdocs
    '''


    def __init__(self,dm_task,owner,login_user):
        '''
        Constructor
        '''
        self.login_user=login_user
        self.owner=owner
        self.task=dm_task
    
    
    def owner_name(self):
        result=self.owner.username
        if self.owner.last_name and self.owner.first_name:
            result=self.owner.last_name+self.owner.first_name
        if self.owner.email:
            result=result+" ("+self.owner.email[:len(self.owner.email)-9]+")"
        return result
    
    def owner_avatar(self):
        result="/static/global/images/fruit-avatar/Fruit-1.png"
        if self.owner.extend_info:
            result=AccountService.get_avatar_url(self.owner)
        return result
    
    def is_owner(self):
        result=""
        task_owners=self.task_owners()
        if len(task_owners):
            owner_ids=[owner.id for owner in task_owners]
            if self.owner.id in owner_ids:
                result="fa-check"
            else:
                result=""
        return result
    
    
    def task_owners(self):
        owners=list()
        if self.task.Owner:
            if self.task.Owner.endswith(','):
                for ownerid in eval(self.task.Owner):
                    tmp_user=User.objects.get(id=ownerid)
                    owners.append(tmp_user)
            else:
                tmp_user=User.objects.get(id=self.task.Owner)
                owners.append(tmp_user)
        return owners
    

        
        