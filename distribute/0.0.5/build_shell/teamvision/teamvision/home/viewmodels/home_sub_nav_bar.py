#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''

class HomeProjectSubNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        self.request=request
        self.all_active=""
        if args['sub_nav_action'] == 'all':
            self.all_active="left_sub_meun_active"
            self.active_product_id="0"
        else:
            self.all_active=""
            self.active_product_id=int(args['sub_nav_action'])
        self.products=args['products']


class HomeAutoTaskSubNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        self.request=request
        self.all_active=""
        self.member_active=""
        self.webhook_active=""
        self.set_menuitem_active(args['sub_nav_action'])
    
    def set_menuitem_active(self,item_name):
        
        if item_name.upper()=="ALL":
            self.all_active="left_sub_meun_active"
            
        if item_name.upper()=="UI":
            self.ui_active="left_sub_meun_active"
        
        if item_name.upper()=="INTERFACE":
            self.interface_active="left_sub_meun_active"


class HomeTaskSubNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        self.request=request
        self.all_active=""
        self.set_menuitem_active(args['sub_nav_action'])
        self.sub_nav_action=args['sub_nav_action']
        self.tasks=args['tasks']
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


class HomeFortestingSubNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        self.request=request
        self.all_active=""
        self.set_menuitem_active(args['sub_nav_action'])
        self.fortestings=args['fortestings']
    
    def set_menuitem_active(self,item_name):
        
        if item_name.upper()=="ALL":
            self.all_active="left_sub_meun_active"

class HomeIssueSubNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        self.request=request
        self.all_active=""
        self.set_menuitem_active(args['sub_nav_action'])
        self.issues=args['issues']
    
    def set_menuitem_active(self,item_name):
        
        if item_name.upper()=="ALL":
            self.all_active="left_sub_meun_active"
        if str(item_name)=="1":
            self.angin2me_active="left_sub_meun_active"
        if str(item_name)=="2":
            self.reportbyme_active="left_sub_meun_active"

class HomeWebappsSubNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        self.request=request
        self.set_menuitem_active(args['sub_nav_action'])
        self.webapps=args['webapps']
    
    def set_menuitem_active(self,item_name):      
        if item_name.upper()=="ALL":
            self.all_active="left_sub_meun_active"




    