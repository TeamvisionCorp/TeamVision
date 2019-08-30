#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''

class CITaskSubNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        self.request=request
        if args['sub_nav_action'] == 'all':
            self.all_active="left_sub_meun_active"
            self.active_product_id="0"
        else:
            self.all_active=""
            self.active_product_id=int(args['sub_nav_action'])
        self.products=args['products']


class CIDeployTaskSubNavBar(CITaskSubNavBar):
    
    def __init__(self,request,**args):
        CITaskSubNavBar.__init__(CIDeployTaskSubNavBar,request,**args)
        self.menu_name="deploy"
        self.sub_bar_title="部署任务"


class CIBuildTaskSubNavBar(CITaskSubNavBar):
    
    def __init__(self,request,**args):
        CITaskSubNavBar.__init__(CIBuildTaskSubNavBar,request,**args)
        self.menu_name="build"
        self.sub_bar_title="构建任务"

class CITestingTaskSubNavBar(CITaskSubNavBar):
    
    def __init__(self,request,**args):
        CITaskSubNavBar.__init__(CITestingTaskSubNavBar,request,**args)
        self.menu_name="testing"
        self.sub_bar_title="测试任务"

class CIServiceSubNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        self.request=request
        if args['sub_nav_action'] == 'all':
            self.all_active="left_sub_meun_active"
            self.active_product_id="0"
        else:
            self.all_active=""
            self.active_product_id=int(args['sub_nav_action'])
        self.products=args['products']

class CISettingsSubNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        self.request=request
        if args['sub_nav_action'] == 'servers':
            self.server_active="left_sub_meun_active"
        
        if args['sub_nav_action'] == 'agent':
            self.agent_active="left_sub_meun_active"
            
        if args['sub_nav_action'] == 'credentials':
            self.credentials_active="left_sub_meun_active"
            
        if args['sub_nav_action'] == 'global_variable':
            self.global_settings_active="left_sub_meun_active"
        
        if args['sub_nav_action'] == 'tags':
            self.tags_active="left_sub_meun_active"






    