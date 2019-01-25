#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''

class ENVSettingsSubNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,env_id,**args):
        self.request=request
        self.env_id=str(env_id)
        self.basic_active=""
        self.member_active=""
        self.webhook_active=""
        self.set_menuitem_active(args['sub_nav_action'])
    
    def set_menuitem_active(self,item_name):
        
        if item_name.upper()=="BASIC":
            self.basic_active="left_sub_meun_active"
            
        if item_name.upper()=="MEMBER":
            self.member_active="left_sub_meun_active"
        
        if item_name.upper()=="WEBHOOK":
            self.webhook_active="left_sub_meun_active"

class ENVFortestingSubNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,env_id,**args):
        self.request=request
        self.env_id=str(env_id)
        self.all_active=""
        self.fortestings=args['fortestings']
        self.set_menuitem_active(args['sub_nav_action'])
    
    def set_menuitem_active(self,item_name):
        
        if item_name.upper()=="ALL":
            self.all_active="left_sub_meun_active"


class ENVVersionSubNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,env_id,**args):
        self.request=request
        self.env_id=str(env_id)
        self.all_active=""
        self.set_menuitem_active(args['sub_nav_action'])
    
    def set_menuitem_active(self,item_name):
        
        if item_name.upper()=="ALL":
            self.all_active="left_sub_meun_active"
            

class ENVTaskSubNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,env_id,**args):
        self.request=request
        self.env_id=str(env_id)
        self.all_active=""
        self.set_menuitem_active(args['sub_nav_action'])
        self.tasks=args['tasks']
        
    
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



    