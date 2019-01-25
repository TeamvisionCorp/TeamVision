#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from doraemon.pagefactory.worker import Worker
from django.template import RequestContext
from doraemon.auth_extend.user.viewmodels.vm_user import VM_User
from business.auth_user.user_service import UserService
from doraemon.auth_extend.user.pagefactory.user_template_path import UserCommonPath

class UserCommonControllPageWorker(Worker):
    '''
    项目页面生成器
    '''
    
    def __init__(self,request):
        Worker.__init__(self, request)
    
    def get_user_dropdown_list(self,selected_user_id):
        vm_users=list()
        for dm_user in UserService.all_users():
            temp_user=VM_User(dm_user,selected_user_id)
            vm_users.append(temp_user)
        pagefileds={"users":vm_users}
        return self.get_webpart(pagefileds,UserCommonPath.user_dropdown_controll)
        
        
        
    