#coding=utf-8
'''
Created on 2014-12-8

@author: zhangtiande
'''

from dataaccess.testjob.dal_testjobhistory import DAL_TestJobHistory
from doraemon.testjob.models import TestJobHistory

# import sys,imp
# imp.reload(sys)
# sys.setdefaultencoding('utf-8')

class TestJobHistoryService(object):
    ''''
    business for Test build
    '''
    
    @staticmethod
    def dm_addbuildhistory(testjob,operator):
        jobhistory=TestJobHistoryService.dm_initbuildhistory(testjob,operator)
        DAL_TestJobHistory.addjobhistory(jobhistory)
     
    @staticmethod
    def dm_initbuildhistory(testjob,operator):
        jobhistory = TestJobHistory()
        jobhistory.TJHJobID=testjob.id
        jobhistory.TJHAutoCaseCounts=testjob.TJAutoCaseCounts
        jobhistory.TJHBugCounts=testjob.TJBugCounts
        jobhistory.TJHCodeLines=testjob.TJCodeLines
        jobhistory.TJHEndTime=testjob.TJEndTime
        jobhistory.TJHIsActive=testjob.TJIsActive
        jobhistory.TJHJobComments=testjob.TJJobComments
        jobhistory.TJHProgress=testjob.TJProgress
        jobhistory.TJHStartTime=testjob.TJStartTime
        jobhistory.TJHStatus=testjob.TJStatus
        jobhistory.TJHTester=testjob.TJTester
        jobhistory.TJHTestPointCounts=testjob.TJTestPointCounts
        jobhistory.TJHOperator=operator
        return jobhistory
         
        