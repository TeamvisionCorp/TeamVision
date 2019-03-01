#coding=utf-8
'''
Created on 2015-11-27

@author: zhangtiande
'''

class VM_Webapps(object):
    '''
    classdocs
    '''


    def __init__(self,webapp,login_user):
        '''
        Constructor
        '''
        self.user=login_user
        self.webapp=webapp
    
    def is_public(self):
        result=False
        if self.webapp.app_visable_level==1:
            result=True
        return result
        