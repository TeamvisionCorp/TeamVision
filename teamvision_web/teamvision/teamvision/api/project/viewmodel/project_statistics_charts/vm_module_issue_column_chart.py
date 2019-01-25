#coding=utf-8
'''
Created on 2018-01-09

@author: zhangtiande
'''

from teamvision.project.models import Version,ProjectModule
from teamvision.api.project.viewmodel.project_statistics_charts.vm_highchart import VM_HighChart
from business.project.issue_statistics_service import IssueStatisticsService
from business.auth_user.user_service import UserService


class ModuleIssueColumnChart(VM_HighChart):
    '''
    classdocs
    '''
    def __init__(self,project_id,version_id,date_range=30):
        '''
        Constructor
        '''
        VM_HighChart.__init__(ModuleIssueColumnChart,project_id, version_id)
        self.chart_id=1
        self.chart_type="column"
        self.chart_title="各模块问题分布"
        self.chart_sub_title="问题在各个模块比例"
        self.xaxis=self.chart_xaxis()
        self.yaxis=self.chart_yaxis()
        self.yaxis_title=""
        self.tooltip=self.chart_tooltip()
        self.series_data=self.series()
    
    def chart_xaxis(self):
        module_name=list()
        module_ids=self.module_ids()
        for module_id in module_ids:
            dm_module=ProjectModule.objects.get(module_id)
            module_name.append(dm_module.Name)
        return module_name
    
    def module_ids(self):
        module_issue_list=IssueStatisticsService.issue_count_byproperty(self.project_id,self.version_id,4)
        module_ids=list()
        for data in module_issue_list:
            if not data['DimensionValue'] in module_ids:
                module_ids.append(data['DimensionValue'])
        return module_ids
        

        
            
        
    def chart_yaxis(self):
        result=list()
        return result
    
    def chart_tooltip(self):
        return ""
    
    def series(self):
        result=list()
        module_issue_count=self.get_module_issue('问题数量')
        result.append(module_issue_count)
        return result
    
    def get_module_issue(self,column_name):
        result=dict()
        result['name']=column_name
        result['data']=list()
        module_issue_list=IssueStatisticsService.issue_count_byproperty(self.project_id,self.version_id,4)
        for data in module_issue_list:
            result['data'].append(data['TotalCount'])   
        return result
        
        
            
        