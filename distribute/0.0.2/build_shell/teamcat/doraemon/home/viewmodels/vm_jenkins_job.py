#coding=utf-8
'''
Created on 2015-12-2

@author: zhangtiande
'''


class VM_JenkinsJob(object):
    
    def __init__(self,job_url,job_parameters):
        self.job_url=job_url
        self.job_parameters=job_parameters
    
    def jenkins_server(self):
        result=""
        if self.job_url:
            job_url=self.job_url.replace("http://","")
            urls=job_url.split("/")
            result=urls[0]
        return result
    
    def job_view(self):
        result=""
        if self.job_url and "view" in self.job_url:
            job_url=self.job_url.replace("http://","")
            urls=job_url.split("/")
            result=urls[3]
        return result
            
    
    def job_name(self):
        result=""
        job_url=self.job_url.replace("http://","")
        urls=job_url.split("/")
        if self.job_url:
            if "view" in self.job_url:
                result=urls[5]
            else:
                result=urls[3]
        return result
    
    def build_url(self,fortesting_id):
        return "http://"+self.jenkins_server()+"/jenkins/mpttrigger/build?mptjob="+self.job_name()+"&mptid="+fortesting_id+"&"+self.job_parameters
