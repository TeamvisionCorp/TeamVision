#coding=utf-8
'''
Created on 2014-9-26

@author: zhangtiande
'''
from django.contrib.auth.models import User

class DAL_User(object):
    '''
    dal for user objects
    '''
    
    @staticmethod
    def getuserbygroup(groupname):
        ''' get user by group name
        '''
        users=[user for user in User.objects.all() if user.groups.filter(name=groupname)]
        return users
    
    @staticmethod
    def getallusers():
        return User.objects.all()
    
    @staticmethod
    def getuser(userid):
        return User.objects.all().get(id=userid)