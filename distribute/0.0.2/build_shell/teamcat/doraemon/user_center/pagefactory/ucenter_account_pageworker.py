#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from doraemon.user_center.pagefactory.ucenter_pageworker import UserCenterPageWorker
from doraemon.user_center.pagefactory.ucenter_template_path import UCenterAccountPath
from doraemon.user_center.viewmodels.ucenter_left_nav_bar import UCenterAccountLeftNavBar
from doraemon.user_center.viewmodels.ucenter_sub_nav_bar import UCenterAccountSubNavBar
from doraemon.user_center.viewmodels.vm_account import VM_Account
import random

class UCenterAccountPageWorker(UserCenterPageWorker):
    '''
    项目页面生成器
    '''
    
    def __init__(self,request):
        '''
        Constructor
        '''
        UserCenterPageWorker.__init__(self, request)
        
        self.left_nav_bar_model=UCenterAccountLeftNavBar
        self.subpage_model=UCenterAccountSubNavBar
    
    def get_account_basic_page(self,request,userid, sub_nav_action):
        sub_leftnav=self.get_account_sub_navbar(request,userid,sub_nav_action)
        left_nav_bar=self.get_account_left_bar(request,userid,sub_nav_action)
        user_info=self.get_account_user_info(request)
        pagefileds={'left_nav_bar':left_nav_bar,'sub_nav_bar':sub_leftnav,"user_form":user_info}
        return self.get_page(pagefileds,UCenterAccountPath.ucenter_account_index,request)
    
    
    def get_account_password_page(self,request,userid, sub_nav_action):
        sub_leftnav=self.get_account_sub_navbar(request,userid,sub_nav_action)
        left_nav_bar=self.get_account_left_bar(request,userid,sub_nav_action)
        password_webpart=self.get_account_password_webpart()
        pagefileds={'left_nav_bar':left_nav_bar,'sub_nav_bar':sub_leftnav,"password_webpart":password_webpart}
        return self.get_page(pagefileds,UCenterAccountPath.ucenter_account_index,request)
    
    def get_account_password_webpart(self):
        return self.get_webpart_none_args(UCenterAccountPath.ucenter_account_password)
        
    
    
    def get_account_avatar_page(self,request,userid,sub_nav_action):
        sub_leftnav=self.get_account_sub_navbar(request,userid,sub_nav_action)
        left_nav_bar=self.get_account_left_bar(request,userid,sub_nav_action)
        avatar_info=self.get_account_avatar_part(request)
        pagefileds={'left_nav_bar':left_nav_bar,'sub_nav_bar':sub_leftnav,"avatar_info":avatar_info}
        return self.get_page(pagefileds,UCenterAccountPath.ucenter_account_index,request)
    
    
    def get_account_left_bar(self,request,userid, sub_nav_action):
        
        return self.get_left_nav_bar(request,self.left_nav_bar_model,userid,UCenterAccountPath.ucenter_account_left_nav,sub_nav_action=sub_nav_action)
    
    def get_account_sub_navbar(self,request,userid, sub_nav_action):
        
        return self.get_sub_nav_bar(request, self.subpage_model, userid,UCenterAccountPath.ucenter_account_subnav,sub_nav_action=sub_nav_action)
    
    def get_account_user_info(self,request):
        vm_account=VM_Account(request.user)
        pagefileds={'account':vm_account}
        return self.get_webpart(pagefileds,UCenterAccountPath.ucenter_account_basic)
    
    def get_account_avatar_part(self,request):
        vm_account=VM_Account(request.user)
        message=request.GET.get('message',"")
        account_avatar=request.GET.get('account_avatar',"")
        if account_avatar:
            vm_account.avatar_url=account_avatar
        pagefileds={'account':vm_account,"form_error":message,"ststem_avatar_counts":[i for i in range(1,21)]}
        return self.get_webpart(pagefileds,UCenterAccountPath.ucenter_account_avatar)
            
        
    
  
    