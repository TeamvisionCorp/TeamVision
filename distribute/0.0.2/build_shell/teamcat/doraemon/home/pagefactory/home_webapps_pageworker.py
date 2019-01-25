#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from doraemon.home.pagefactory.pageworker import DevicePageWorker
from doraemon.home.viewmodels.home_left_nav_bar import HomeWebAppsLeftNavBar
from doraemon.home.viewmodels.home_sub_nav_bar import HomeWebappsSubNavBar
from doraemon.home.viewmodels.vm_webapps import VM_Webapps
from doraemon.home.pagefactory.home_template_path import HomeWebappsPath
from business.home.webapp_service import WebappService


class HomeWebappsPageWorker(DevicePageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self,request):
        '''
        Constructor
        '''
        DevicePageWorker.__init__(self, request)
        self.side_bar_model=HomeWebAppsLeftNavBar
        self.sub_side_bar_model=HomeWebappsSubNavBar
    
    def get_full_page(self,request,sub_nav_action):
        webapp_list=WebappService.get_webapps(request)
        sub_nav_bar=self.get_webapps_sub_navbar(request,sub_nav_action,webapp_list)
        left_nav_bar=self.get_webapps_left_bar(request,sub_nav_action)
        webapp_webpart=self.get_webapp_webpart(request, webapp_list)
        webapp_create_dialog=self.get_webapp_create_dialog(request)
        page_fileds={'left_nav_bar':left_nav_bar,'sub_leftnav':"","webapp_webpart":webapp_webpart,"webapp_create_dialog":webapp_create_dialog}
        return self.get_page(page_fileds,HomeWebappsPath.webapps_index_path,request)
    
    def get_webapps_left_bar(self,request,sub_nav_action):
        return self.get_left_nav_bar(request,self.side_bar_model,HomeWebappsPath.left_nav_template_path,sub_nav_action=sub_nav_action)
    
    def get_webapps_sub_navbar(self,request,sub_nav_action,webapps):
        print(sub_nav_action)
        return self.get_sub_nav_bar(request,self.sub_side_bar_model,HomeWebappsPath.sub_nav_template_path,sub_nav_action=sub_nav_action,webapps=webapps)
    
    def get_webapp_webpart(self,request,webapp_lists):
        vm_webapps=self.get_webapp_vm_list(webapp_lists, request.user)
        pagefileds={"webapps":vm_webapps}
        return self.get_webpart(pagefileds,HomeWebappsPath.webapps_webpart_path)
    
    def get_webapp_create_dialog(self,request):
        return self.get_webpart_none_args(HomeWebappsPath.webapps_create_dialog_path)
    
    def get_webapp_vm_list(self,webapps,login_user):
        result=list()
        for webapp in webapps:
            tmp_webapp=VM_Webapps(webapp,login_user)
            result.append(tmp_webapp)
        return result
    