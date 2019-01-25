#coding=utf-8
'''
Created on 2015-11-17

@author: zhangtiande
'''
from django.contrib.auth.models import User,Group
from doraemon.auth_extend.user.models import User_Group_Extend
from doraemon.resources.user_service.resource_string import UserService as RUserService
from business.auth_user.permission_service import PermissionService


class SystemRoleService(object):
    '''
    classdocs
    '''
    
    @staticmethod
    def all_roles():
        return Group.objects.all().order_by("id")

    @staticmethod
    def get_role(roleid):
        role=None
        try:
            role=Group.objects.get(id=roleid)
        except Exception as ex:
            print(ex)
        return role
    
    @staticmethod
    def get_role_byname(role_name):
        role=None
        try:
            role=Group.objects.get(name=role_name)
        except Exception as ex:
            print(ex)
        return role
    
    @staticmethod
    def create_role(request):
        role=Group()
        role.name=request.POST.get("group_name")
        role.save()
        SystemRoleService.add_role_extendinfo(role)
    
    @staticmethod
    def delete_role(request,roleid):
        role=SystemRoleService.get_role(roleid)
        role.delete()
    
    
    @staticmethod
    def update_role_permission(request,roleid):
        role=SystemRoleService.get_role(roleid)
        permission_id=request.POST.get("permission_id")
        active=request.POST.get("active")
        temp_permission=PermissionService.get_permission(permission_id)
        if active=="1":
            role.permissions.add(temp_permission)
        if active=="0":
            role.permissions.remove(temp_permission)
        role.save()
    
    
    @staticmethod
    def update_role_description(request,roleid):
        role=SystemRoleService.get_role(roleid)
        role_desc=request.POST.get("role_desc")
        role_extend_info=role.extend_info
        role_extend_info.description=role_desc
        role_extend_info.save()
            
            
        
        
    
    @staticmethod
    def add_role_extendinfo(role):
        role_extend=User_Group_Extend()
        role_extend.backcolor="#32be77"
        role_extend.group_id=role.id
        role_extend.group_priority=0
        role_extend.save()
    
    @staticmethod
    def check_rolename_exists(request):
        result=False
        value=request.POST.get("value","")
        role=Group.objects.get(name=value)
        if role:
            result=True
        return result
    
    
    

        
                                                                      
            
            
        
        
        