#coding=utf-8
# coding=utf-8
'''
Created on 2014-2-16

@author: ETHAN
'''
from dataaccess.testjob.dal_testsubmition import DAL_TestSubmition
from doraemon.testjob.viewmodels.vm_testsubmition import VM_TestSubmition
from dataaccess.common.dal_dictvalue import DAL_DictValue
from business.common.userservice import UserService
from business.testjob.testsubmitionservice import TestSubmitionService
import datetime

class VM_TestJob(object):
    '''
    TestJOB business model
    '''
    
    def __init__(self,job,loginuser):
        ''' dm_testjob wapper
        '''
        self.testjob=job
        self.user=loginuser
        
    def get_submitionid(self):
        submitionid="--"
        if self.testjob.TJSubmitionID:
            submitionid=str(self.testjob.TJSubmitionID)
        return submitionid
    
    def get_job_name(self):
        jobname="--"
        if self.testjob.TJJobName:
            jobname=self.testjob.TJJobName
        return jobname
    
    def get_job_submit_time(self):
        submitiontime="--"
        try:
            dm_submition=TestSubmitionService.getsubmition(self.testjob.TJSubmitionID)
            vm_submition=VM_TestSubmition(dm_submition,self.user)
            submitiontime=vm_submition.getsubmitiontime()[:11]
        except Exception,ex:
            print ex
        return submitiontime
    
    
    def get_startdate(self):
        startdate="--"
        if self.testjob.TJStartTime:
            startdate=str(self.testjob.TJStartTime+datetime.timedelta(hours=8))[:11]
        return startdate
    
    def get_enddate(self):
        enddate="--"
        if self.testjob.TJEndTime:
            enddate=str(self.testjob.TJEndTime+datetime.timedelta(hours=8))[:11]
        return enddate
    
    def get_finished_date(self):
        finisheddate="--"
        if self.testjob.TJFinishedTime:
            finisheddate=str(self.testjob.TJFinishedTime+datetime.timedelta(hours=8))[:11]
        return finisheddate
    
    def get_job_progress(self):
        return str(self.testjob.TJProgress)+"%"
    
    def get_job_status(self):
        status="--"
        statusobject=DAL_DictValue.getdatavaluebyid(self.testjob.TJStatus)
        if statusobject:
            status=statusobject.DicDataName
        return status
    
    def get_job_tester(self):
        testnames=list()
        result=""
        if self.testjob.TJTester:
            testerlist=eval(self.testjob.TJTester)
            for testerid in testerlist:
                tester=UserService.getuser(testerid)
                testername=tester.last_name+tester.first_name
                if testername not in testnames:
                    result=result+testername+" "
        return result
    
    def get_submition_type(self):
        result=0
        try:
            dm_submition=TestSubmitionService.getsubmition(self.testjob.TJSubmitionID)
            result=dm_submition.TPSProductType
        except Exception,ex:
            pass
        return result
    
    def can_change_job(self):
        result=False
        if self.user.has_perm('testjob.change_testjob'):
            result=True
        return result
    
    def create_child_job(self):
        result=False
        if self.user.has_perm('testjob.create_child_job'):
            result=True
        return result
    