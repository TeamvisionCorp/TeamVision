#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''

class ProjectSettingsSubNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,projectid,**args):
        self.request=request
        self.projectid=str(projectid)
        self.basic_active=""
        self.member_active=""
        self.webhook_active=""
        self.version_active=""
        self.module_active=""
        self.set_menuitem_active(args['sub_nav_action'])
    
    def set_menuitem_active(self,item_name):
        
        if item_name.upper()=="BASIC":
            self.basic_active="left_sub_meun_active"
            
        if item_name.upper()=="VERSION":
            self.version_active="left_sub_meun_active"
        
        if item_name.upper()=="MODULE":
            self.module_active="left_sub_meun_active"
            
        if item_name.upper()=="MEMBER":
            self.member_active="left_sub_meun_active"
        
        if item_name.upper()=="WEBHOOK":
            self.webhook_active="left_sub_meun_active"

class ProjectFortestingSubNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,projectid,**args):
        self.request=request
        self.projectid=str(projectid)
        self.all_active=""
        self.fortestings=args['fortestings']
        self.set_menuitem_active(args['sub_nav_action'])
    
    def set_menuitem_active(self,item_name):
        
        if item_name.upper()=="ALL":
            self.all_active="left_sub_meun_active"


class ProjectVersionSubNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,projectid,**args):
        self.request=request
        self.projectid=str(projectid)
        self.all_active=""
        self.set_menuitem_active(args['sub_nav_action'])
    
    def set_menuitem_active(self,item_name):
        
        if item_name.upper()=="ALL":
            self.all_active="left_sub_meun_active"
            

class ProjectTaskSubNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,projectid,**args):
        self.request=request
        self.projectid=str(projectid)
        self.all_active=""
        self.set_menuitem_active(args['sub_nav_action'])
        self.tasks=args['tasks']
        self.sub_nav_action=args['sub_nav_action']
        self.members=args['members']
        
    
    def set_menuitem_active(self,item_name):
        
        if item_name.upper()=="ALL":
            self.all_active="left_sub_meun_active"
        
        if item_name.upper()=="PROCESS":
            self.process_active="left_sub_meun_active"
        if item_name.upper()=="CREATEBYME":
            self.createbyme_active="left_sub_meun_active"
        
        if item_name.upper()=="ASGINME":
            self.asgin2me_active="left_sub_meun_active"


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



    