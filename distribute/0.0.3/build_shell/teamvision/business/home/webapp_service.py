#coding=utf-8
'''
Created on 2015-11-27

@author: zhangtiande
'''
from teamvision.home.models import WebApps
from django.contrib.admin.models import DELETION,CHANGE,ADDITION
import random

class WebappService(object):
    '''
    classdocs
    '''
    
    @staticmethod
    def get_webapps(request):
        public_apps= WebApps.objects.all().filter(app_visable_level=1)
        my_apps=WebApps.objects.all().filter(app_creator=request.user.id).exclude(app_visable_level=1)
        return public_apps | my_apps
    
    @staticmethod
    def create_webapp(request):
        webapp=WebApps()
        webapp.app_title=request.POST.get("app_title")
        webapp.app_creator=request.user.id
        webapp.app_key=request.POST.get("app_key")
        webapp.app_url=request.POST.get("app_url")
        webapp.app_visable_level=2
        webapp.app_avatar="/static/global/images/caton/caton"+str(random.randint(1, 30))+".jpeg"
        webapp.save()
        WebappService.log_create_activity(request.user,webapp)
    
    @staticmethod
    def remove_webapp(request):
        webapp_id=request.POST.get("webapp_id")
        webapp=WebApps.objects.get(webapp_id)
        webapp.IsActive=0
        webapp.save()
        WebappService.log_delete_activity(request.user,webapp)
    
    
    @staticmethod
    def log_create_activity(user,target):
        WebApps.objects.log_action(user.id,target.id,target.app_title,ADDITION,"创建了新工具",0)
    
    @staticmethod
    def log_delete_activity(user,target):
        WebApps.objects.log_action(user.id,target.id,target.app_title,DELETION,"删除了工具",0)
        