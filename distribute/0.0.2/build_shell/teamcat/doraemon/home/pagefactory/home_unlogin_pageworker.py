#coding=utf-8
#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from doraemon.home.pagefactory.pageworker import DevicePageWorker
from doraemon.home.pagefactory.home_device_pageworker import HomeDevicePageWorker
from doraemon.home.pagefactory.home_template_path import Home_unloginPagePath


class HomeUnloginPageWorker(DevicePageWorker):
    '''
    项目页面生成器
    '''
    def __init__(self,request):
        '''
        Constructor
        '''
        DevicePageWorker.__init__(self, request)
        self.login_background="#FFF"

    def get_welcome_page(self,request):
        welcome_webpart=self.get_webpart_none_args(Home_unloginPagePath.home_welcome_path)
        pagefileds={"login_background":self.login_background,"welcome_page":welcome_webpart,"request":request}
        return self.get_page(pagefileds,Home_unloginPagePath.home_page_path, request)
    
    def project_summary_page(self,request):
        project_summary_webpart=self.get_webpart_none_args(Home_unloginPagePath.home_project_summary_path)
        pagefileds={"login_background":self.login_background,"project_summary_page":project_summary_webpart,}
        return self.get_page(pagefileds,Home_unloginPagePath.home_page_path, request)
    
    
    def device_summary_page(self,request):
        page_worker=HomeDevicePageWorker(request)
        device_list_webpart=page_worker.get_device_list_page(request)
        pagefileds={"login_background":self.login_background,"devicelist":device_list_webpart}
        return self.get_page(pagefileds,Home_unloginPagePath.home_device_page_path, request)
    
        
        
    