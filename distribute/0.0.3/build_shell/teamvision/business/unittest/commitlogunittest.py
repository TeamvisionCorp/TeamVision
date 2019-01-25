#coding=utf-8
'''
Created on 2014-12-19

@author: Devuser
'''
import unittest
# from business.testjob.codecommitlogservice import CodeCommitLogService
from business.common.jenkinsservice import JenkinsService


class Test(unittest.TestCase):


    def testupdatsvncommitlog(self):
        pass
#         CodeCommitLogService.update_svn_commit_log(45)
    
    def test_jenkins_job(self):
        print(JenkinsService.getjenkinsjobs("10.3.254.34:8080"))
    
    def test_trigger_jenkins_job(self):
        print(JenkinsService.trigerbuild("10.3.254.34:8080","http://10.3.254.34:8080/jenkins/mpttrigger/build?mptjob=Develop-Android-NGA&mptid=397"))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testupdatsvncommitlog']
    unittest.main()