#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from doraemon.logcat.pagefactory.pageworker import LogcatPageWorker
from doraemon.home.viewmodels.home_left_nav_bar import HomeDeviceLeftNavBar
from doraemon.logcat.pagefactory.logcat_template_path import LogcatPagePath
from doraemon.logcat.pagefactory.logcat_template_path import LogcatCommonPath
from business.logcat.logger_service import LoggerService
from doraemon.logcat.models import Logger
from doraemon.logcat.viewmodels.vm_logger import VM_Logger
# from business.project.project_service import ProjectService

class LoggerPageWorker(LogcatPageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self,request):
        '''
        Constructor
        '''
        LogcatPageWorker.__init__(self, request)
        self.pagemodel=HomeDeviceLeftNavBar
        
    
    def get_logger_fullpage(self,request):

        logger_list=self.get_logger_list_page(request)
        pagefileds={'left_nav_bar':"","logger_list":logger_list}
        return self.get_page(pagefileds,LogcatPagePath.logger_page_path,request)

    
    
    def get_logger_list_page(self,request):
        logger_controll_list=self.get_logger_list_controll()
        logger_content_container=self.get_logger_content_container(request)
        pagefileds={"logger_controll_list":logger_controll_list,"logger_content_container":logger_content_container}
        return self.get_webpart(pagefileds,LogcatPagePath.logger_list_page)
    
    def get_logger_list_controll(self,):
        dm_loggers=Logger.objects.all().order_by("-id")
        vm_loggers=list()
        for dm_logger in dm_loggers:
            vm_logger=VM_Logger(dm_logger)
            vm_loggers.append(vm_logger)
        pagefileds={"loggers":vm_loggers}
        web_part=self.get_webpart(pagefileds,LogcatPagePath.logger_list_controll)
        return web_part
    
    def more_businesslog(self,request):
        index=request.POST.get('index',0)
        device_id=request.POST.get("device_id")
        start_index=int(index)*20
        end_index=start_index+20
        result=LoggerService.get_more_logs(device_id, start_index, end_index)
        return result
    
    
    def get_logger_content_container(self,request):
        pagefileds={}
        web_part=self.get_webpart(pagefileds,LogcatPagePath.logger_content_container)
        return web_part
        
    
        
        