#coding=utf-8
'''
Created on 2015-11-17

@author: zhangtiande
'''
from django.contrib.auth.models  import Permission
from teamvision.auth_extend.user.models import User_Permission_Extend
from dataaccess.auth_user.dal_permission import DAL_Permission

class PermissionService(object):
    '''
    classdocs
    '''
    
    
    @staticmethod
    def all_custom_permissions():
        return DAL_Permission.get_all_custom_permission()
        
    @staticmethod
    def all_permissions():
        return Permission.objects.all()
        

    @staticmethod
    def get_permission(permission_id):
        permission=None
        try:
            permission=Permission.objects.get(id=permission_id)
        except Exception as ex:
            print(ex)
        return permission
                                                                               
    
    @staticmethod
    def create_permission(request):
        new_permission=Permission()
        new_permission.content_type_id=1
        new_permission.codename=request.POST.get("codename")
        new_permission.name=request.POST.get("permission_title")
        new_permission.save()
        description=request.POST.get("permission_desc")
        permission_type=request.POST.get("permission_type")
        new_permission.save()
        PermissionService.create_permission_extend(new_permission.id,permission_type, description)
        
    
    @staticmethod
    def create_permission_extend(permission_id,permission_type,description):
        permission_extend=User_Permission_Extend()
        permission_extend.Description=description
        permission_extend.PermissionType=permission_type
        permission_extend.permission_id=permission_id
        permission_extend.save()
        
        
    @staticmethod    
    def delete_permission(request):
        permission_id=request.POST.get("permission_id","")
        permission=Permission.objects.get(id=permission_id)
        permission.delete()
        
    
    @staticmethod    
    def update_permission_name(request,permission_id):
        permission=Permission.objects.get(id=permission_id)
        permission.name=request.POST.get("permission_name")
        permission.save()
    
    @staticmethod    
    def update_permission_desc(request,permission_id):
        permission=Permission.objects.get(id=permission_id)
        description=request.POST.get("permission_desc")
        extend_info=permission.extend_info
        extend_info.Description=description
        extend_info.save()
    
        
    @staticmethod
    def check_codename_exists(request):
        result=False
        value=request.POST.get("value","")
        permission=Permission.objects.get(codename=value)
        if permission:
            result=True
        return result
            
        
        
        
        
    
                                                                      
            
            
        
        
        