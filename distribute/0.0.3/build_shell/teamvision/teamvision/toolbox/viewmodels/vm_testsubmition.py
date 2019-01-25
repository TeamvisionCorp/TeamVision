#coding=utf-8
# coding=utf-8
'''
Created on 2014-2-16

@author: ETHAN
'''

from dataaccess.common.dal_dictvalue import DAL_DictValue
from business.common.userservice import UserService
from dataaccess.testjob.dal_testjob import DAL_TestJob
import time
import datetime

class VM_TestSubmition(object):
    '''
    TestSubmition business model
    '''
    
    def __init__(self,submition,loginuser):
        ''' dm_testsubmition wapper
        '''
        self.testsubmition=submition
        self.user=loginuser
    
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
    def getsubmitorgroup(self):
        grouplist=list()
        user=UserService.getuser(self.testsubmition.TPSSubmiter)
        for group in user.groups.all():
            if group.name not in grouplist:
                grouplist.append(group.name)
        return grouplist

    def is_job_finished(self):
        result=False
        try:
            testjobs=DAL_TestJob.getjobsbysubmitionid(self.testsubmition.id)
            if len(testjobs):
                result= testjobs[0].TJProgress=='100'
            else:
                result= False
        except Exception,ex:
            print(ex)
        return result
    
    def can_process_submition(self):
        result=False
        if self.user.has_perm('testjob.can_process_submition'):
            result=True
        return result
    
    def can_change_submition(self):
        result=False
        if self.user.has_perm('testjob.change_testprojectsubmition'):
            result=True
        return result
    
    def can_submit_submition(self):
        result=False
        if self.user.has_perm('testjob.can_submit_testing'):
            result=True
        return result
    
    def can_add_submition(self):
        result=False
        if self.user.has_perm('testjob.add_testprojectsubmition'):
            result=True
        return result
    
    def can_delete_submition(self):
        result=False
        if self.user.has_perm('testjob.delete_testprojectsubmition'):
            result=True
        return result
        
        