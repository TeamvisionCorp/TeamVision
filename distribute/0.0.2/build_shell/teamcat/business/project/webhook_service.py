#coding=utf-8
'''
Created on 2015-11-17

@author: zhangtiande
'''

from doraemon.project.models import WebHook
from django.contrib.admin.models import DELETION,CHANGE,ADDITION
from gatesidelib.httplibhelper import HttpLibHelper
from doraemon.home.viewmodels.vm_jenkins_job import VM_JenkinsJob
from business.common.jenkinsservice import JenkinsService

class WebHookService(object):
    '''
    classdocs
    '''


    @staticmethod
    def get_webhooks(project_id):
        return WebHook.objects.all(project_id).order_by("-id")
    
    @staticmethod
    def add_webhook(request,projectid):
        dm_webhook=WebHook()
        project_webhook=WebHookService.init_webhook(request, projectid, dm_webhook)
        WebHookService.un_default_webhook(projectid,project_webhook.WHCatagory)
        project_webhook.WHCreator=request.user.id
        project_webhook.WHIsDefault=1
        project_webhook.save()
        WebHookService.log_create_activity(request.user,project_webhook)
    
    
    @staticmethod
    def edit_webhook(request,projectid,webhook_id):
        dm_webhook=WebHook.objects.get(webhook_id)
        project_webhook=WebHookService.init_webhook(request, projectid, dm_webhook)
        project_webhook.save()
        WebHookService.log_edit_activity(request.user,project_webhook)
    
    
    @staticmethod
    def remove_webhook(request,webhook_id):
        project_webhook=WebHook.objects.get(webhook_id)
        project_webhook.IsActive=0
        project_webhook.save()
        WebHookService.log_delete_activity(request.user,project_webhook)
    
    @staticmethod
    def set_webhook_default(request,project_id,webhookid):
        webhook=WebHook.objects.get(webhookid)
        WebHookService.un_default_webhook(project_id, webhook.WHCatagory)
        webhook.WHIsDefault=1
        webhook.save()
    
    @staticmethod
    def init_webhook(request,projectid,dm_webhook):
        project_webhook=dm_webhook
        project_webhook.WHCatagory=1
        project_webhook.WHLabel=request.POST.get("WHLabel","")
        project_webhook.WHParameters=request.POST.get("WHParameters","")
        project_webhook.WHURL=request.POST.get("WHURL")
        project_webhook.WHProjectID=projectid
        return project_webhook
    
    @staticmethod
    def un_default_webhook(project_id,webhook_catrory):
        webhooks=WebHook.objects.all(project_id).filter(WHCatagory=webhook_catrory)
        for webhook in webhooks:
            webhook.WHIsDefault=0
            webhook.save();
            
    
    @staticmethod
    def perform_hook(request,webhook_id):
        webhook=WebHook.objects.get(webhook_id)
        vm_jenkins_job=VM_JenkinsJob(webhook.WHURL,webhook.WHParameters)
        JenkinsService.trigerbuild(vm_jenkins_job.jenkins_server(),vm_jenkins_job.build_url("0"))
        
        
    @staticmethod
    def log_create_activity(user,target):
        WebHook.objects.log_action(user.id,target.id,target.WHLabel,ADDITION,"添加了WebHook",target.WHProjectID)
    
    @staticmethod
    def log_edit_activity(user,target):
        WebHook.objects.log_action(user.id,target.id,target.WHLabel,ADDITION,"修改了WebHook",target.WHProjectID)
    
    @staticmethod
    def log_delete_activity(user,target):
        WebHook.objects.log_action(user.id,target.id,target.WHLabel,DELETION,"删除了WebHook",target.WHProjectID)
        
        