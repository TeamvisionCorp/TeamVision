#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''

from teamvision.project.models import Project

class ProjectLeftNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,projectid):
        self.request=request
#         self.dashboard_href='/project/'+str(projectid)+'/dashboard'
        self.task_href='/project/'+str(projectid)+'/task/'
        self.settings_href='/project/'+str(projectid)+'/settings/basic'
        self.fortesting_href='/project/'+str(projectid)+'/fortesting'
        self.version_href='/project/'+str(projectid)+'/version'
        self.archive_href='/project/'+str(projectid)+'/archive/all'
        self.issue_href='/project/'+str(projectid)+'/issue/all'
        self.statistics_href='/project/'+str(projectid)+'/statistics/all'
        self.project=Project.objects.get(projectid)


class menuitem(object):
    
    def __init__(self,namevalue,keyvalue):
        self.key=keyvalue
        self.name=namevalue
    
    def get_name(self):
        return self.name
    
    def get_key(self):
        return self.key
    
    def get_id(self):
        return "123456"

class ProjectTaskLeftNavBar(ProjectLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,projectid,**args):
        ProjectLeftNavBar.__init__(self,request,projectid)
        self.request=request
        self.task_href='/project/'+str(projectid)+'/task/'+args['sub_nav_action']
        self.task_active="leftmeunactive"
        self.custom_menu_list=list()
        
class ProjectDashboardLeftNavBar(ProjectLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,projectid,**args):
        ProjectLeftNavBar.__init__(self,request,projectid)
        self.request=request
        self.dashboard_active="leftmeunactive"
        self.custom_menu_list=list()

class ProjectSettingsLeftNavBar(ProjectLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,projectid,**args):
        ProjectLeftNavBar.__init__(self,request,projectid)
        self.request=request
        self.settings_href='/project/'+str(projectid)+'/settings/'+args['sub_nav_action']
        self.settings_active="leftmeunactive"
        self.custom_menu_list=list()

class ProjectForTestingLeftNavBar(ProjectLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,projectid,**args):
        ProjectLeftNavBar.__init__(self,request,projectid)
        self.request=request
        self.fortesting_href='/project/'+str(projectid)+'/fortesting/'+args['sub_nav_action']
        self.fortesting_active="leftmeunactive"
        self.custom_menu_list=list()


class ProjectArchiveLeftNavBar(ProjectLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,projectid,**args):
        ProjectLeftNavBar.__init__(self,request,projectid)
        self.request=request
        self.archive_href='/project/'+str(projectid)+'/archive/'+args['sub_nav_action']
        self.archive_active="leftmeunactive"
        self.custom_menu_list=list()

class ProjectIssueLeftNavBar(ProjectLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,projectid,**args):
        ProjectLeftNavBar.__init__(self,request,projectid)
        self.request=request
        self.issue_href='/project/'+str(projectid)+'/issue/'+args['sub_nav_action']
        self.issue_active="leftmeunactive"
        self.custom_menu_list=list()

class ProjectStatisticsLeftNavBar(ProjectLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,projectid,**args):
        ProjectLeftNavBar.__init__(self,request,projectid)
        self.request=request
        self.statistics_href='/project/'+str(projectid)+'/statistics/'+args['sub_nav_action']
        self.statistics_active="leftmeunactive"
        self.custom_menu_list=list()



class ProjectVersionLeftNavBar(ProjectLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,projectid,**args):
        ProjectLeftNavBar.__init__(self,request,projectid)
        self.request=request
        self.version_href='/project/'+str(projectid)+'/version'
        self.version_active="leftmeunactive"
        self.custom_menu_list=list()

    