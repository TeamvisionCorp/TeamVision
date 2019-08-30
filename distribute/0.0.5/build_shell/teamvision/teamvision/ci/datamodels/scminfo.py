#coding=utf-8
'''
Created on 2014-12-18

@author: Devuser
'''

class SCMInfo(object):
    '''
    classdocs
    '''


    def __init__(self,scm_user,scm_password,local_dir):
        '''
        info for access scm server
        
        '''
        self.scmuser=scm_user
        self.scmpassword=scm_password
        self.localdir=local_dir
        