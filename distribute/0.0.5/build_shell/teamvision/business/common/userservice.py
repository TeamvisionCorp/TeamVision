#coding=utf-8
'''
Created on 2014-10-8

@author: zhangtiande
'''
from dataaccess.common.dal_user import DAL_User
from business.business_service import BusinessService

class UserService(BusinessService):
    
    @staticmethod
    def get_user(userid):
        user=None
        try:
            user=DAL_User.getuser(userid)
        except Exception as ex:
            print(ex)
        return user
    
    @staticmethod
    def getusersbygroup(usergroup):
        return DAL_User.getuserbygroup(usergroup)
    
    @staticmethod
    def getalluseremaillist():
        emaillist=list()
        for user in DAL_User.getallusers():
            emaillist.append(user.email)
        return emaillist
        