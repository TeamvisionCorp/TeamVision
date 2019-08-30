#coding=utf-8
'''
Created on 2015-11-18

@author: Devuser
'''

class VM_User(object):
    '''
    classdocs
    '''


    def __init__(self,user,selected_user_id):
        '''
        Constructor
        '''
        self.user=user
        self.selected_user_id=selected_user_id
    
    
    def user_name(self):
        result=self.user.username
        if self.user.last_name and self.user.first_name:
            result=self.user.last_name+self.user.first_name
        if self.user.email:
            result=result+" ("+self.user.email+")"
        return result
    
    def is_selected(self):
        result="";
        if self.user.id==self.selected_user_id:
            result="selected"
        return result
            