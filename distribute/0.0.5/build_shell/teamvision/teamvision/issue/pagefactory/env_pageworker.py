#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from teamvision.pagefactory.worker import Worker
from django.template import RequestContext
from teamvision.project.models import Project
from teamvision.project.pagefactory.project_template_path import  ProjectCommonControllPath
from business.project.project_service import ProjectService

class ENVPageWorker(Worker):
    '''
    项目页面生成器
    '''
    def __init__(self,request):
        '''
        Constructor
        '''
        Worker.__init__(self, request)
    
    def get_left_nav_bar(self,request,pageModel,env_id,template_path,**args):
        page=pageModel(request,env_id,**args)
        context_fileds={'page':page}
        return self.get_webpart(context_fileds,template_path)
    
    def get_sub_nav_bar(self,request,pageModel,env_id,template_path,**args):
        
        page=pageModel(request,env_id,**args)
        context_fileds={'page':page}
        return self.get_webpart(context_fileds,template_path)
    
    def get_full_page_with_header(self,request,pagefileds,env_id,template_path):
        header_project_group=self.get_header_project_menu(request, env_id)
        pagefileds["header_project_group"]=header_project_group
        return self.get_page(pagefileds, template_path, request)
        
    def get_header_env_menu(self,request,env_id):
        project=Project.objects.get(env_id)
        project_menu_control=self.get_env_menu(request,ProjectCommonControllPath.header_project_control_path)
        pagefileds= {"project":project,"header_project_menu":project_menu_control}
        return self.get_webpart(pagefileds,ProjectCommonControllPath.header_project_menu_path)
    
    def get_env_menu(self,request,project_control_path):
        projects=list()
        for project in ProjectService.get_projects_include_me(request):
            projects.append(project)
        pagefileds={"projects":projects}
        return self.get_webpart(pagefileds,project_control_path)
        
        