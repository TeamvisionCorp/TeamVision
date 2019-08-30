#coding=utf-8
'''
Created on 2015-11-4

@author: Devuser
'''
from django.shortcuts import HttpResponse

from teamvision.ci.models import CITask,CITaskHistory
from teamvision.home.models import Agent
from django.contrib.auth.models import User
from business.ucenter.account_service import AccountService
from gatesidelib.datetimehelper import DateTimeHelper
import datetime
from gatesidelib.common.simplelogger import SimpleLogger

class VM_CITaskQueue(object):
    '''
    classdocs
    '''
    
    def __init__(self,dm_task_queue):
        self.ci_task_queue=dm_task_queue
        self.ci_task=self.get_task()
    
    def get_task(self):
        return CITask.objects.get(self.ci_task_queue.TaskID)
    
    def build_version(self):
        result=0
        history=CITaskHistory.objects.get_by_tqid(self.ci_task_queue.id)
        if history:
            result=history.BuildVersion
        return str(result)
    
    def task_type_name(self):
        result="deploy"
        
        if self.ci_task.TaskType==1:
            result="testing"
        
        if self.ci_task.TaskType==4:
            result="build"
        
        if self.ci_task.TaskType==5:
            result="deploy"
        return result
    
    def agent_name(self):
        result=""
        if self.ci_task_queue.AgentID:
            result=Agent.objects.get(self.ci_task_queue.AgentID).Name
        return result
    
    def start_by_avatar(self):
        result="/static/global/images/caton/caton1.jpeg"
        try:
            ci_task_history=CITaskHistory.objects.get_history_by_tq(self.ci_task_queue.id)
            started_by=User.objects.get(id=ci_task_history.StartedBy)
            if started_by.extend_info:
                result=AccountService.get_avatar_url(started_by)
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    def start_by_name(self):
        result="系统定时任务"
        try:
            ci_task_history=CITaskHistory.objects.get_history_by_tq(self.ci_task_queue.id)
            started_by=User.objects.get(id=ci_task_history.StartedBy)
            result=started_by.last_name+started_by.first_name
        except Exception as ex:
            print(ex)
        return result
    
    def build_progress(self):
        result=20
        if self.ci_task_queue:
            if self.ci_task_queue.StartTime:
                start_time=self.ci_task_queue.StartTime+datetime.timedelta(hours=8)
                duration=DateTimeHelper.get_time_to_now(str(start_time)[:19],"%Y-%m-%d %H:%M:%S")
                result=int(duration)/10
                if result>90:
                    result=90
                elif result<0:
                    result=5
            else:
                result=5
        return result
        
    
    
    