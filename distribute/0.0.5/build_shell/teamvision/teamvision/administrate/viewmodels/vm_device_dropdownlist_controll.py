#coding=utf-8
'''
Created on 2015-11-4

@author: zhangtiande
'''
from django.shortcuts import HttpResponse
from teamvision.project.models import Project,Tag
from django.contrib.auth.models import User
from business.ucenter.account_service import AccountService

class VM_DropDownControll(object):
    '''
    classdocs
    '''
    
    def __init__(self,dicdata,selected_value):
        self.dicdata=dicdata
        self.selected_value=selected_value
    
    def selected(self):
        result=""
        if self.dicdata.DicDataValue==self.selected_value:
            result="selected"
        return result
            