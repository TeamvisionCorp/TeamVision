#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''


class CITestingTaskPropertyNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        self.request=request
        self.ci_task=args['ci_task']
        if args['property_nav_action'] == 'history':
            self.result_active="left_sub_meun_active"
        
        if args['property_nav_action'] == 'config':
            self.config_active="left_sub_meun_active"
            
        if args['property_nav_action'] == 'parameter':
            self.parameter_active="left_sub_meun_active"
        
        if args['property_nav_action'] == 'build':
            self.build_active="left_sub_meun_active"
        
        if args['property_nav_action'] == 'build_clean':
            self.build_clean_active="left_sub_meun_active"


class CITaskPropertyNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        self.request=request
        self.ci_task=args['ci_task']
        if args['property_nav_action'] == 'history':
            self.history_active="left_sub_meun_active"
            
        if args['property_nav_action'] == 'unittest_history':
            self.unittest_active="left_sub_meun_active"
        
        if args['property_nav_action'] == 'config':
            self.config_active="left_sub_meun_active"
            
        if args['property_nav_action'] == 'parameter':
            self.parameter_active="left_sub_meun_active"
        
        if args['property_nav_action'] == 'build':
            self.build_active="left_sub_meun_active"
        
        if args['property_nav_action'] == 'changelog':
            self.changelog_active="left_sub_meun_active"
        
        if args['property_nav_action'] == 'build_clean':
            self.build_clean_active="left_sub_meun_active"






    