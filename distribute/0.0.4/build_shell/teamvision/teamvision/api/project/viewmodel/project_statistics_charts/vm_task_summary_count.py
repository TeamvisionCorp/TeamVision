#coding=utf-8
'''
Created on 2018-01-09

@author: zhangtiande
'''

from business.project.task_statistics_service import TaskStatisticsService

class VM_TaskSummaryCount(object):
    '''
    classdocs
    '''

    def __init__(self,project_id,version_id,request):
        '''
        Constructor
        '''
        self.chart_id=0
        self.project_id=project_id
        self.version_id=version_id
        self.request = request
        self.today_finished_count = self.get_today_finished_tcount()
        self.delayed_count = self.get_delayed_tcount()
        self.delay_finished_count = self.get_delay_finished_tcount()


    def get_today_finished_tcount(self):
        status_data = TaskStatisticsService.task_finished_today(self.project_id,self.version_id,self.request)
        return status_data

    def get_delayed_tcount(self):
        status_data = TaskStatisticsService.task_delayed_today(self.project_id, self.version_id,self.request)
        return status_data

    def get_delay_finished_tcount(self):
        status_data = TaskStatisticsService.task_delayed_finished_today(self.project_id, self.version_id,self.request)
        return status_data



        