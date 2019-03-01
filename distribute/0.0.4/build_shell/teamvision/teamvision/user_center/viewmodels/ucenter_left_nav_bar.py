#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''

class UCenterLeftNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,userid):
        self.request=request
        self.account_href='/ucenter/'+str(userid)+'/account/basic'


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

class UCenterAccountLeftNavBar(UCenterLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,userid,**args):
        UCenterLeftNavBar.__init__(self,request,userid)
        self.request=request
        self.account_href='/ucenter/'+str(userid)+'/account/'+args['sub_nav_action']
        self.account_active="leftmeunactive"
        self.custom_menu_list=list()
        
class ProjectDashboardLeftNavBar(UCenterLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,projectid,**args):
        UCenterLeftNavBar.__init__(self,request,projectid)
        self.request=request
        self.dashboard_active="leftmeunactive"
        self.custom_menu_list=list()

class ProjectSettingsLeftNavBar(UCenterLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,projectid,**args):
        UCenterLeftNavBar.__init__(self,request,projectid)
        self.request=request
        self.settings_href='/project/'+str(projectid)+'/settings/'+args['sub_nav_action']
        self.settings_active="leftmeunactive"
        self.custom_menu_list=list()

class ProjectForTestingLeftNavBar(UCenterLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,projectid,**args):
        UCenterLeftNavBar.__init__(self,request,projectid)
        self.request=request
        self.fortesting_href='/project/'+str(projectid)+'/fortesting/'+args['sub_nav_action']
        self.fortesting_active="leftmeunactive"
        self.custom_menu_list=list()

class ProjectVersionLeftNavBar(UCenterLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,projectid,**args):
        UCenterLeftNavBar.__init__(self,request,projectid)
        self.request=request
        self.version_href='/project/'+str(projectid)+'/version'
        self.version_active="leftmeunactive"
        self.custom_menu_list=list()

    