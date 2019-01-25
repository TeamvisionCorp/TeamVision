#coding=utf-8
'''
Created on 2015-11-17

@author: Devuser
'''

from business.auth_user.user_service import UserService
from doraemon.project.models import ProjectMember,Project
from django.contrib.admin.models import DELETION,CHANGE,ADDITION
from django.contrib.auth.models import User

class MemberService(object):
    '''
    classdocs
    '''


    @staticmethod
    def get_member_users(project_id):
        dm_members=ProjectMember.objects.get_members(project_id)
        user_ids=[member.PMMember for member in dm_members ]
        return UserService.all_users().filter(id__in=user_ids).order_by("email")
    
    @staticmethod
    def add_member(member_id,projectid,operator):
        project_member=ProjectMember()
        project_member.PMProjectID=projectid
        project_member.PMMember=member_id
        project_member.PMRoleID=1
        project_member.PMRoleType=1
        project_member.save()
        MemberService.log_create_activity(operator,project_member)
    
    @staticmethod
    def remove_member(request,projectid):
        user_id=request.POST.get("PMMember")
        project_member=ProjectMember.objects.get_member(projectid,user_id)
        project_member.IsActive=0
        project_member.save()
        MemberService.log_delete_activity(request.user,project_member)
    
    @staticmethod
    def update_role(request,projectid,userid):
        member_id=ProjectMember.objects.get_member(projectid, userid).id
        project_member=ProjectMember.objects.get(member_id)
        project_member.PMRoleID=request.POST.get("PMRoleID",1)
        project_member.save()
    
    
    @staticmethod
    def log_create_activity(user,target):
        member=User.objects.get(id=target.PMMember)
        ProjectMember.objects.log_action(user.id,target.id,member.username,ADDITION,"添加了成员",target.PMProjectID)
    
    @staticmethod
    def log_delete_activity(user,target):
        member=User.objects.get(id=target.PMMember)
        ProjectMember.objects.log_action(user.id,target.id,member.username,DELETION,"删除了成员",target.PMProjectID)
        
        