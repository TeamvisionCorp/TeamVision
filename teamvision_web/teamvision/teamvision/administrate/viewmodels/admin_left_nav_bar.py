#coding=utf-8
'''
Created on 2015-9-24

@author: zhangtiande
'''

class AdminLeftNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request):
        self.request=request
        self.user_href='/administrate/user/all'
        self.system_role_href='/administrate/systemrole/all'
        self.permission_href='/administrate/permission/all'
        self.device_href='/administrate/device/all'

class AdminUserLeftNavBar(AdminLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        AdminLeftNavBar.__init__(self,request)
        self.request=request
        self.user_href='/administrate/user/'+args['sub_nav_action']
        self.user_active="leftmeunactive"
        self.custom_menu_list=list()

class AdminSystemRoleLeftNavBar(AdminLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        AdminLeftNavBar.__init__(self,request)
        self.request=request
        self.system_role_href='/administrate/systemrole/'+args['sub_nav_action']
        self.system_role_active="leftmeunactive"
        self.custom_menu_list=list()

class AdminPermissionLeftNavBar(AdminLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        AdminLeftNavBar.__init__(self,request)
        self.request=request
        self.permission_href='/administrate/permission/'+args['sub_nav_action']
        self.permission_active="leftmeunactive"
        self.custom_menu_list=list()

class AdminDeviceLeftNavBar(AdminLeftNavBar):
    '''
    classdocs
    '''
    def __init__(self,request,**args):
        AdminLeftNavBar.__init__(self,request)
        self.request=request
        self.device_href='/administrate/device/'+args['sub_nav_action']
        self.device_active="leftmeunactive"
        self.custom_menu_list=list()
        


    