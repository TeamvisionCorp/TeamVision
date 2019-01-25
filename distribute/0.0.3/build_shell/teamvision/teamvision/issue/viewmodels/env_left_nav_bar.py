#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''

from teamvision.interface.models import ENV

class ENVLeftNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,envid):
        self.request=request
        self.dashboard_href='/env/'+str(envid)+'/dashboard'
        self.task_href='/env/'+str(envid)+'/task/all'
        self.settings_href='/env/'+str(envid)+'/settings/basic'
        self.fortesting_href='/env/'+str(envid)+'/fortesting/all'
        self.version_href='/env/'+str(envid)+'/version'
        self.archive_href='/env/'+str(envid)+'/archive/all'
        self.env=ENV.objects.get(envid)


        
class ENVDashboardLeftNavBar(ENVLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,envid,**args):
        ENVLeftNavBar.__init__(self,request,envid)
        self.request=request
        self.dashboard_active="leftmeunactive"
        self.custom_menu_list=list()

class ENVSettingsLeftNavBar(ENVLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,envid,**args):
        ENVLeftNavBar.__init__(self,request,envid)
        self.request=request
        self.settings_href='/env/'+str(envid)+'/settings/'+args['sub_nav_action']
        self.settings_active="leftmeunactive"
        self.custom_menu_list=list()

class ENVForTestingLeftNavBar(ENVLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,envid,**args):
        ENVLeftNavBar.__init__(self,request,envid)
        self.request=request
        self.fortesting_href='/env/'+str(envid)+'/fortesting/'+args['sub_nav_action']
        self.fortesting_active="leftmeunactive"
        self.custom_menu_list=list()


class ENVArchiveLeftNavBar(ENVLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,envid,**args):
        ENVLeftNavBar.__init__(self,request,envid)
        self.request=request
        self.archive_href='/env/'+str(envid)+'/archive/'+args['sub_nav_action']
        self.archive_active="leftmeunactive"
        self.custom_menu_list=list()



class ENVVersionLeftNavBar(ENVLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,envid,**args):
        ENVLeftNavBar.__init__(self,request,envid)
        self.request=request
        self.version_href='/env/'+str(envid)+'/version'
        self.version_active="leftmeunactive"
        self.custom_menu_list=list()

    