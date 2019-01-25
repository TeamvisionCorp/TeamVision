#coding=utf-8
#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from doraemon.interface.pagefactory.env_pageworker import ENVPageWorker
from doraemon.interface.viewmodels.env_left_nav_bar import ENVLeftNavBar
from doraemon.interface.pagefactory.env_template_path import ENVPortalPath


from business.project.project_service import ProjectService

class ENVPortalPageWorker(ENVPageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self,request):
        '''
        Constructor
        '''
        ENVPageWorker.__init__(self, request)
        self.pagemodel=ENVLeftNavBar
        self.sub_sidebar_model=None
        
    
    def get_env_fullpage(self,request,sub_nav_action):
        dm_envs=ProjectService.get_projects_include_me(request,sub_nav_action)
        dm_products=ProjectService.get_products_include_me(request)
#         left_nav_bar=self.get_project_left_bar(request, sub_nav_action)
#         sub_nav_bar=self.get_project_sub_nav_bar(request,dm_projects,sub_nav_action,dm_products)
        list2=[i for i in range(6)]
        env_list=self.get_env_control(request,list2)
        pagefileds={'left_nav_bar':"","sub_nav_bar":"","web_appview":self.get_env_portal_webapp(env_list)}
        return self.get_page(pagefileds,ENVPortalPath.portal_index,request)
    
    def get_env_left_bar(self,request,sub_nav_action):
        return self.get_left_nav_bar(request,self.pagemodel,ENVPortalPath.left_nav_template_path,sub_nav_action=sub_nav_action)
    
    
    def get_env_sub_nav_bar(self,request,dm_envs,sub_nav_action,products):
        return self.get_sub_nav_bar(request,self.sub_sidebar_model,ENVPortalPath.sub_nav_template_path,sub_nav_action=sub_nav_action,envs=dm_envs,products=products)
    
    def get_env_portal_webapp(self,env_list):
        pagefileds={'env_list':env_list}
        return self.get_webpart(pagefileds,ENVPortalPath.env_portal_webapp_path)
    
    def get_env_list_page(self,request,dm_envs):
        envs=list()
        for env in dm_envs:
#             tem_env=VM_env(request.user,False,env,0)
            envs.append(None)
        env_list_control=self.get_env_control(request, envs)
        pagefileds={"envs":envs,"env_list":env_list_control}
        return self.get_webpart(pagefileds,ENVPortalPath.env_list_template_path)
    
    
    def get_portal_env_list(self,request):
#         dm_envs=envService.get_envs_include_me(request,None)
        dm_envs=list()
        envs=list()
        for env in dm_envs:
            if env !=None:
#                 tem_env=VM_env(request.user,False,env,0)
                envs.append(None)
        env_list_control=self.get_env_control(request, envs)
        return env_list_control
    
      
    
    def get_env_control(self,request,envs):
        pagefileds={"envs":envs}
        return self.get_webpart(pagefileds,ENVPortalPath.env_list_control_path)
        
        
        