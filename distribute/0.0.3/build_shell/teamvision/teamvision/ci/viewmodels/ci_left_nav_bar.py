#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''

class CILeftNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request):
        self.request=request
        self.ci_href='/ci/task'
        self.deploy_href='/ci/taskflow'
        self.build_href='/ci/build/all'
        self.testing_href='/ci/testing/all'
        self.service_href='/ci/service/all'
        self.settings_href='/ci/settings/global_variable'

class CIDeployLeftNavBar(CILeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        CILeftNavBar.__init__(self,request)
        self.request=request
#         self.deploy_href='/home/project/'+args['sub_nav_action']
        self.deploy_active="leftmeunactive"
        self.custom_menu_list=list()
        
class CIDashboardLeftNavBar(CILeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        CILeftNavBar.__init__(self,request)
        self.request=request
        self.dashboard_active="leftmeunactive"
        self.custom_menu_list=list()

class CIBuildLeftNavBar(CILeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        CILeftNavBar.__init__(self,request)
#         self.build_href='/home/autotask/'+args['sub_nav_action']
        self.request=request
        self.build_active="leftmeunactive"
        self.custom_menu_list=list()

class CITestingLeftNavBar(CILeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        CILeftNavBar.__init__(self,request)
#         self.build_href='/home/autotask/'+args['sub_nav_action']
        self.request=request
        self.test_active="leftmeunactive"
        self.custom_menu_list=list()



class CIServiceLeftNavBar(CILeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        CILeftNavBar.__init__(self,request)
        self.request=request
#         self.fortesting_href='/home/fortesting/'+args['sub_nav_action']
        self.service_active="leftmeunactive"
        self.custom_menu_list=list()

class CISettingsLeftNavBar(CILeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        CILeftNavBar.__init__(self,request)
        self.request=request
#         self.task_href='/home/task/'+args['sub_nav_action']
        self.settings_active="leftmeunactive"
        self.custom_menu_list=list()
        

    