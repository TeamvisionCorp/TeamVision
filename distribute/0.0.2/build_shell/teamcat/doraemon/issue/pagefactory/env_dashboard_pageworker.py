#coding=utf-8
#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from doraemon.interface.pagefactory.env_pageworker import ENVPageWorker
from doraemon.interface.viewmodels.env_left_nav_bar import ENVDashboardLeftNavBar
from doraemon.interface.pagefactory.env_template_path import ENVDashBoardPath


from business.project.project_service import ProjectService

class ENVDashBoardPageWorker(ENVPageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self,request):
        '''
        Constructor
        '''
        ENVPageWorker.__init__(self, request)
        self.pagemodel=ENVDashboardLeftNavBar
        self.sub_sidebar_model=None
        
    
    def get_dashboard_index(self,request,sub_nav_action):
        dm_envs=ProjectService.get_projects_include_me(request,sub_nav_action)
        dm_products=ProjectService.get_products_include_me(request)
        left_nav_bar=self.get_dashboard_left_bar(request, sub_nav_action)
        list2=[i for i in range(60)]
        env_list=""
        pagefileds={'left_nav_bar':left_nav_bar,"sub_nav_bar":"","web_appview":self.get_dashboard_webapp(env_list)}
        return self.get_page(pagefileds,ENVDashBoardPath.dashboard_index,request)
    
    def get_dashboard_left_bar(self,request,sub_nav_action):
        return self.get_left_nav_bar(request,self.pagemodel,1,ENVDashBoardPath.left_nav_template_path,sub_nav_action=sub_nav_action)
    
    
    def get_dashboard_sub_nav_bar(self,request,dm_envs,sub_nav_action,products):
        return self.get_sub_nav_bar(request,self.sub_sidebar_model,1,ENVDashBoardPath.sub_nav_template_path,sub_nav_action=sub_nav_action,envs=dm_envs,products=products)
    
    def get_dashboard_webapp(self,env_list):
        pagefileds={'env_list':env_list}
        return self.get_webpart(pagefileds,ENVDashBoardPath.env_dashboard_webapp_path)
        
        
        