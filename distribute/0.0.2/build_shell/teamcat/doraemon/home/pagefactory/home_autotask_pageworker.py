#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from doraemon.home.pagefactory.pageworker import DevicePageWorker
from doraemon.home.viewmodels.home_left_nav_bar import HomeAutoTestingTaskLeftNavBar
from doraemon.home.viewmodels.home_sub_nav_bar import HomeAutoTaskSubNavBar
from doraemon.home.pagefactory.home_template_path import HomeAutoTaskPath

class HomeAutoTaskPageWorker(DevicePageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.pagemodel=HomeAutoTestingTaskLeftNavBar
        self.sub_sidebar_model=HomeAutoTaskSubNavBar
        
    
    def get_autotask_fullpage(self,request,sub_nav_action):
        left_nav_bar=self.get_autotask_left_bar(request, sub_nav_action)
        sub_nav_bar=self.get_autotask_sub_nav_bar(request, sub_nav_action)
        autotask_list=self.get_autotask_list(request, sub_nav_action)
        pagefileds={'left_nav_bar':left_nav_bar,"sub_nav_bar":sub_nav_bar,"auto_task_list":autotask_list}
        return self.get_page(pagefileds,'autotask/home_autotask_index.html',request)
    
    def get_autotask_left_bar(self,request,sub_nav_action):
        return self.get_left_nav_bar(request,self.pagemodel,HomeAutoTaskPath.left_nav_template_path,sub_nav_action=sub_nav_action)
    
    
    def get_autotask_sub_nav_bar(self,request,sub_nav_action):
        return self.get_sub_nav_bar(request,self.sub_sidebar_model,HomeAutoTaskPath.sub_nav_template_path,sub_nav_action=sub_nav_action)
    
    def get_autotask_list(self,request,sub_nav_action):
        return self.get_page_none_args(HomeAutoTaskPath.project_list_template_path)
    