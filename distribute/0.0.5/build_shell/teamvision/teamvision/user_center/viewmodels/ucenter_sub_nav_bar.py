#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''

class UCenterAccountSubNavBar(object):
    '''
    classdocs
    '''
    def __init__(self,request,userid,**args):
        self.request=request
        self.userid=str(userid)
        self.basic_active=""
        self.password_active=""
        self.webhook_active=""
        self.set_menuitem_active(args['sub_nav_action'])
    
    def set_menuitem_active(self,item_name):
        
        if item_name.upper()=="BASIC":
            self.basic_active="left_sub_meun_active"
            
        if item_name.upper()=="PASSWORD":
            self.password_active="left_sub_meun_active"



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



    