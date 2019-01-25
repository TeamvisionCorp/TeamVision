#coding=utf-8
'''
Created on 2018-01-09

@author: zhangtiande
'''

from doraemon.project.models import Version
from doraemon.api.project.viewmodel.project_statistics_charts.vm_highchart import VM_HighChart
from business.project.issue_statistics_service import IssueStatisticsService
from business.auth_user.user_service import UserService


class UnClosedIssueColumnChart(VM_HighChart):
    '''
    classdocs
    '''
    def __init__(self,project_id,version_id,date_range=30):
        '''
        Constructor
        '''
        VM_HighChart.__init__(UnClosedIssueColumnChart,project_id, version_id)
        self.chart_id=1
        self.chart_type="column"
        self.chart_title="剩余问题分布"
        self.chart_sub_title="剩余问题人员分布"
        self.xaxis=self.chart_xaxis()
        self.yaxis=self.chart_yaxis()
        self.yaxis_title=""
        self.tooltip=self.chart_tooltip()
        self.series_data=self.series()
    
    def chart_xaxis(self):
        user_name=list()
        user_ids=self.issue_owner()
        # user_ids=user_ids+self.issue_owner(5)
        # user_ids=user_ids+self.issue_owner(4)
        for user_id in user_ids:
            if str(user_id)!='1':
                dm_user=UserService.get_user(user_id)
                user_name.append(dm_user.last_name+dm_user.first_name)
        return user_name
    
    def issue_owner(self):
        unclosed_issue_list=IssueStatisticsService.unclosed_issue_count(self.project_id, self.version_id)
        print(unclosed_issue_list)
        user_ids=list()
        for data in unclosed_issue_list:
            if not data['Processor'] in user_ids and str(data['Processor']) !='1':
                user_ids.append(data['Processor'])
        return user_ids
        

    def chart_yaxis(self):
        result=list()
        return result
    
    def chart_tooltip(self):
        return ""
    
    def series(self):
        result=list()
        new_issue_count=self.get_issue_total('New')
        reopened_issue_count=self.get_issue_total('Reopened')
        resloved_issue_count=self.get_issue_total("Resolved")
        result.append(new_issue_count)
        result.append(reopened_issue_count)
        result.append(resloved_issue_count)
        return result
    
    def get_issue_total(self,column_name):
        result=dict()
        result['name']=column_name
        result['data']=list()
        if column_name=="New":
            '''status 2'''
            result['data']=self.get_issue_bystatus(2)
                    
        if column_name=="Reopened":
            '''status 5'''
            result['data']=self.get_issue_bystatus(5)
            
        if column_name=="Resolved":
            '''status 4'''
            result['data']=self.get_issue_bystatus(4)
            
        return result
    
    def get_issue_bystatus(self,status):
        unclosed_issue_list=IssueStatisticsService.unclosed_issue_count(self.project_id, self.version_id,status)
        user_ids=self.issue_owner()
        result=list()
        for user_id in user_ids:
            flag=False
            for data in unclosed_issue_list:
                if str(user_id)==str(data['Processor']) and str(user_id)!='1':
                    result.append(data['TotalCount'])
                    flag=True
                    break
            if not flag:
                result.append(0)        
        return result
        
        
            
        