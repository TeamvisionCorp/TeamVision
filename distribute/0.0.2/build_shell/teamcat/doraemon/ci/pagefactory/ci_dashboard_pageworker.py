#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from doraemon.ci.pagefactory.ci_pageworker import CIPageWorker
from doraemon.ci.viewmodels.ci_left_nav_bar import CIDashboardLeftNavBar

from doraemon.home.models import TaskQueue
from doraemon.ci.viewmodels.vm_ci_task_queue import VM_CITaskQueue
from doraemon.ci.viewmodels.vm_ci_agent import VM_CIAgent
from business.ci.ci_agent_service import CIAgentService
from business.ci.ci_task_queue_service import CITQService
from doraemon.ci.pagefactory.ci_task_pageworker import CITaskPageWorker
from doraemon import settings
from doraemon.ci.pagefactory.ci_template_path  import CIDashBoardPath,CICommonControllPath
from business.common.redis_service import RedisService
from gatesidelib.common.simplelogger import SimpleLogger
from doraemon.ci.models import CITaskHistory


class CIDashBoardPageWorker(CIPageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self,request):
        '''
        Constructor
        '''
        CIPageWorker.__init__(self, request)
        self.pageModel=CIDashboardLeftNavBar
    
    def get_dashboard_fullpage(self,request):
        task_pageworker=CITaskPageWorker(request)
        left_nav_bar=self.get_dashboard_left_bar(request)
        dashboard_task_queue=self.get_dashboard_task_queue_webpart(request)
        dashboard_task_list=task_pageworker.get_dashboard_task_list_webpart(request)
        dashboard_agent=self.get_dashboard_agent_list_webpart(request)
        pagefileds={"left_nav_bar":left_nav_bar,"dashboard_task_queue":dashboard_task_queue,"dashboard_task_list":dashboard_task_list,"dashboard_agent":dashboard_agent}
        return self.get_page(pagefileds,'dashboard/ci_dashboard_index.html', request)
    
    
    def get_dashboard_left_bar(self,request):
        return self.get_left_nav_bar(request, self.pageModel, CIDashBoardPath.left_nav_template_path)
    
    
#     
    def get_dashboard_task_queue_webpart(self,request):
        ci_dashboard_task_queue=self.get_dashboard_taskqueue_listcontroll(request)
        pagefileds={"ci_dashboard_task_queue":ci_dashboard_task_queue}
        return self.get_webpart(pagefileds,CIDashBoardPath.task_queue_webpart)
    
    
    def get_dashboard_agent_list_webpart(self,request):
        ci_dashboard_agent=self.get_dashboard_agent_list_controll(request)
        page_fileds={"ci_build_status_listcontroll":ci_dashboard_agent}
        return self.get_webpart(page_fileds,CIDashBoardPath.task_build_status_page)
    
    def get_dashboard_agent_list_controll(self,request):
        all_agent=CIAgentService.get_all_agents()
        vm_agents=list()
        for dm_agent in all_agent:
            tmp_agent=VM_CIAgent(dm_agent,0)
            vm_agents.append(tmp_agent)
        page_fileds = {"ci_agents":vm_agents}
        return self.get_webpart(page_fileds,CIDashBoardPath.task_build_status_controll)

    
    def get_dashboard_taskqueue_listcontroll(self,request):
        all_task_queue=CITQService.task_queue_list()
        vm_tq_list=list()
        for tq in all_task_queue:
            temp=VM_CITaskQueue(tq)
            vm_tq_list.append(temp)
        pagefileds={"task_queue_list":vm_tq_list}
        return self.get_webpart(pagefileds,CIDashBoardPath.task_queue_list_controll)        
        
    def ci_build_log_dialog(self,request):
        tq_id=request.POST.get("tq_id",0)
        if not tq_id:
            history_id=request.POST.get("history_id","0");
            tq_id=CITaskHistory.objects.get(int(history_id)).TaskQueueID
        dm_tq=TaskQueue.objects.get(int(tq_id))
        vm_tq=VM_CITaskQueue(dm_tq)
        http_host=request.META['HTTP_HOST']
        ws_url="ws://"+http_host+"/ws/"+str(tq_id)
        web_socket_scripts=self.get_webpart({"WS4REDIS_URI":ws_url,"WS4REDIS_HEARTBEAT":settings.WS4REDIS_HEARTBEAT},CICommonControllPath.ci_build_log_js)
        pagefileds={"ci_build_logs":"","web_socket_scripts":web_socket_scripts,"task_queue":vm_tq }
        return self.get_webpart(pagefileds,CICommonControllPath.ci_build_log_dialog)
    
    def get_build_log_content(self,tq_id):
        result=""
        ci_build_logs=RedisService.get_value("ci_build_log"+tq_id)
        return ci_build_logs
            
         
        
    