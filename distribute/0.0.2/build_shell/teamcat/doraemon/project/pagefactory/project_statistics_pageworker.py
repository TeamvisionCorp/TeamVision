#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from doraemon.project.pagefactory.project_pageworker import ProjectPageWorker
from doraemon.project.viewmodels.project_left_nav_bar import ProjectStatisticsLeftNavBar
from doraemon.project.pagefactory.project_template_path import ProjectStatisticsPath
from doraemon.project.pagefactory.project_common_pageworker import ProjectCommonControllPageWorker
from doraemon.project.viewmodels.project_statistics_charts.vm_issue_status_statistics_chart import IssueStatusStatisticsChart



class ProjectStatisticsPageWorker(ProjectPageWorker):
    '''
    项目页面生成器
    '''

    def __init__(self,request):
        '''
        Constructor
        '''
        ProjectPageWorker.__init__(self, request)
        self.left_nav_bar_model=ProjectStatisticsLeftNavBar
    
    def get_index_page(self,request,projectid):
        left_nav_bar=self.get_issue_left_bar(request,projectid,sub_nav_action="all")
        pagefileds={'left_nav_bar':left_nav_bar,'web_app_view':self.get_web_app(projectid,0)}
        return self.get_full_page_with_header(request, pagefileds, projectid,ProjectStatisticsPath.index_template_path)
    
    def get_web_app(self,project_id,version_id):
        statistics_chart=self.get_statistics_chart_webpart(project_id,version_id)
        pagefileds={'statistics_chart':statistics_chart,'issue_item':""}
        return self.get_webpart(pagefileds,ProjectStatisticsPath.statistics_webapp)
    
    def get_statistics_chart_webpart(self,project_id,version_id):
        issue_status_summary=self.get_statistics_status_summary(project_id,version_id)
        version_dropdownlist=ProjectCommonControllPageWorker.get_version_dropdown_list(self, project_id,version_id)
        pagefileds={'issue_status_summary':issue_status_summary,'version_dropdownlist':version_dropdownlist}
        return self.get_webpart(pagefileds,ProjectStatisticsPath.statistics_chart)
    
    def get_statistics_status_summary(self,project_id,version_id):
        print(version_id)
        issue_status_chart=IssueStatusStatisticsChart(project_id,version_id)
        pagefileds={'issue_status_chart':issue_status_chart}
        return self.get_webpart(pagefileds,ProjectStatisticsPath.statistics_issue_number)
        
    def get_issue_left_bar(self,request,projectid, sub_nav_action):
        return self.get_left_nav_bar(request,self.left_nav_bar_model,projectid,ProjectStatisticsPath.left_nav_template_path,sub_nav_action=sub_nav_action)
    
    
   
        
    