#coding=utf-8
'''
Created on 2015-9-24

@author: zhangtiande
'''

class AdminUserSubNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        self.request=request
        self.all_active=""
        self.set_menuitem_active(args['sub_nav_action'])
        self.users_count=args['users_count']
    
    def set_menuitem_active(self,item_name):
        
        if item_name.upper()=="ALL":
            self.all_active="left_sub_meun_active"

class AdminSystemRoleSubNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        self.request=request
        self.all_active=""
        self.set_menuitem_active(args['sub_nav_action'])
        self.system_role_counts=args['system_role_counts']
    
    def set_menuitem_active(self,item_name):
        
        if item_name.upper()=="ALL":
            self.all_active="left_sub_meun_active"


class AdminPermissionSubNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        self.request=request
        self.all_active=""
        self.set_menuitem_active(args['sub_nav_action'])
    
    def set_menuitem_active(self,item_name):
        
        if item_name.upper()=="ALL":
            self.all_active="left_sub_meun_active"

class AdminDeviceSubNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        self.request=request
        self.all_active=""
        self.lending_active=""
        self.android_active=""
        self.ios_active=""
        self.other_active=""
        self.set_menuitem_active(args['sub_nav_action'])
#         self.device_count=args['device_count']
    
    def set_menuitem_active(self,item_name):
        
        if item_name.upper()=="ALL":
            self.all_active="left_sub_meun_active"
            
        if item_name.upper()=="LENDING":
            self.lending_active="left_sub_meun_active"
            
        if item_name.upper()=="ANDROID":
            self.android_active="left_sub_meun_active"
        
        if item_name.upper()=="IOS":
            self.ios_active="left_sub_meun_active"
        
        if item_name.upper()=="OTHER":
            self.other_active="left_sub_meun_active"





    