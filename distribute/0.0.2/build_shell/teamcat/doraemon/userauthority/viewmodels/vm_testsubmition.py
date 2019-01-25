#coding=utf-8
# coding=utf-8
'''
Created on 2014-2-16

@author: ETHAN
'''

from dataaccess.common.dal_dictvalue import DAL_DictValue
from business.common.userservice import UserService
import time
import datetime

class VM_TestSubmition(object):
    '''
    TestSubmition business model
    '''
    
    def __init__(self,submition):
        ''' dm_testsubmition wapper
        '''
        self.testsubmition=submition
    
    def getproductname(self):
        productname="--"
        product=DAL_DictValue.getdatavaluebyid(self.testsubmition.TPSProductName)
        if product:
            productname=product.DicDataName
        return productname
    
    def getproducttype(self):
        producttype="--"
        producttypeobject=DAL_DictValue.getdatavaluebyid(self.testsubmition.TPSProductType)
        if producttypeobject:
            producttype=producttypeobject.DicDataName 
        return producttype
    
    
    def getstatus(self):
        status="--"
        statusobject=DAL_DictValue.getdatavaluebyid(self.testsubmition.TPSStatus)
        if statusobject:
            status=statusobject.DicDataName
        return status
    
    def getsubmitor(self):
        username="--"
        if self.testsubmition.TPSSubmiter:
            user=UserService.getuser(self.testsubmition.TPSSubmiter)
            username=user.last_name+user.first_name
        return username
            
    def getplatform(self):
        platform="--"
        platformobject=DAL_DictValue.getdatavaluebyid(self.testsubmition.TPSPlatform)
        if platformobject:
            platform=platformobject.DicDataName
        return platform
        
    def getsubmitiontime(self):
        submitiontime="--"
        if self.testsubmition.TPSSubmitTime:
            submitiontime=str(self.testsubmition.TPSSubmitTime+datetime.timedelta(hours=8))[:13]
        return submitiontime
    
    def issubmited(self):
        if self.testsubmition.TPSSubmitTime:
            return 1
        else:
            return 0