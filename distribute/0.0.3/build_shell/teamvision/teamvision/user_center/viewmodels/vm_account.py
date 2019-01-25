#coding=utf-8
'''
Created on 2015-12-28

@author: Devuser
'''
from teamvision.home.models import FileInfo
from business.ucenter.account_service import AccountService

class VM_Account(object):
    '''
    classdocs
    '''


    def __init__(self,user):
        '''
        Constructor
        '''
        self.user=user
        self.avatar_url=""
        self.avatar()
    
    def avatar(self):
        self.avatar_url=AccountService.get_avatar_url(self.user)
        