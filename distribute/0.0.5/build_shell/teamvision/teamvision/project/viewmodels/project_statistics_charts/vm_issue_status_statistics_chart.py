#coding=utf-8
'''
Created on 2018-01-09

@author: zhangtiande
'''

from gatesidelib.datetimehelper import DateTimeHelper
from business.project.issue_statistics_service import IssueStatisticsService


class IssueStatusStatisticsChart(object):
    '''
    classdocs
    '''
    def __init__(self,project_id,version_id):
        '''
        Constructor
        '''
        self.chart_id=1
        self.project_id=project_id
        self.version_id=version_id
    
    
    def new_issue_count(self):
        return IssueStatisticsService.issue_count_bystatus(self.project_id, self.version_id,2)
        
    
    def resloved_issue_count(self):
        return IssueStatisticsService.issue_count_bystatus(self.project_id, self.version_id,4)
    
    def reopened_issue_count(self):
        return IssueStatisticsService.issue_count_bystatus(self.project_id, self.version_id,5)
    
    def closed_issue_count(self):
        return IssueStatisticsService.issue_count_bystatus(self.project_id, self.version_id,3)
    
        
        