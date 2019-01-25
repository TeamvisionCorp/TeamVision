#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from doraemon.project.pagefactory.project_pageworker import ProjectPageWorker
from doraemon.project.pagefactory.project_settings_pageworker import ProjectSettingsPageWorker
from doraemon.project.pagefactory.project_template_path import ProjectSettingsPath
from doraemon.project.models import WebHook
from doraemon.project.viewmodels.vm_webhook import VM_WebHook

from gatesidelib.common.simplelogger import SimpleLogger
from business.project.webhook_service import WebHookService



class WebHookPageWorker(ProjectPageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self,request):
        '''
        Constructor
        '''
        ProjectPageWorker.__init__(self, request)

    
    def get_full_page(self,request,projectid,sub_nav_action):
        setting_page_worker=ProjectSettingsPageWorker(request)
        sub_leftnav=setting_page_worker.get_settings_sub_navbar(request,projectid,sub_nav_action)
        left_nav_bar=setting_page_worker.get_settings_left_bar(request,projectid,sub_nav_action)
        project_info=self.get_webhook_webpart(request,projectid,WebHook())
        pagefileds={'left_nav_bar':left_nav_bar,'sub_leftnav':sub_leftnav,'project_info':project_info}
        return self.get_full_page_with_header(request, pagefileds, projectid,'settings/index.html')
          
    
    def get_edit_page(self,request,projectid,webhook_id):
        setting_page_worker=ProjectSettingsPageWorker(request)
        sub_leftnav=setting_page_worker.get_settings_sub_navbar(request,projectid,"")
        left_nav_bar=setting_page_worker.get_settings_left_bar(request,projectid,"")
        dm_webhook=WebHook.objects.get(webhook_id)
        project_info=self.get_webhook_webpart(request, projectid,dm_webhook)
        pagefileds={'left_nav_bar':left_nav_bar,'sub_leftnav':sub_leftnav,'project_info':project_info}
        return self.get_full_page_with_header(request, pagefileds, projectid,'settings/index.html')      
                    
    
    def get_webhook_webpart(self,request,projectid,dm_webhook):
        webhook_form=self.get_webhook_from(dm_webhook,projectid,request.user)
        dm_webhooks=WebHookService.get_webhooks(projectid)
        webhooks=self.get_webhooks(dm_webhooks, projectid, request.user)
        pagefileds={"webhook_form":webhook_form,"webhooks":webhooks,"is_create":dm_webhook.WHProjectID==None}
        return self.get_webpart(pagefileds,ProjectSettingsPath.project_webhook_template_path)
    
    def get_webhook_from(self,dm_webhook,project_id,login_user):
        webhook=dm_webhook
        vm_webhook=VM_WebHook(project_id,webhook,login_user)
        pagefileds={"webhook":vm_webhook}
        return self.get_webpart(pagefileds, ProjectSettingsPath.project_webhook_form_path)
    
    def get_webhooks(self,dm_webhooks,project_id,login_user):
        result=list()
        for hook in dm_webhooks:
            tmp_hook=VM_WebHook(project_id,hook,login_user)
            result.append(tmp_hook)
        return result
        
        
    
        
    