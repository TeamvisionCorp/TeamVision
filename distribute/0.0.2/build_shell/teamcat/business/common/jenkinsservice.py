#coding=utf-8
'''
Created on 2014-10-8

@author: tiande.zhang
'''
import httplib2
from json.decoder import JSONDecoder
import json
import base64

class JenkinsService():
    
    @staticmethod
    def getjenkinsjobs(jenkinsserver):
        conn = httplib2.HTTPConnectionWithTimeout(jenkinsserver)
        conn.request("GET","/jenkins/api/json")  
        r1 = conn.getresponse()
        data1 = r1.read()
        json_decoder=JSONDecoder()
        conn.close()
        return json_decoder.decode(data1.decode())
    
    @staticmethod
    def getjobinfo(servername,joburl):
        conn = httplib2.HTTPConnectionWithTimeout(servername)
        conn.request("GET",joburl+"api/json")  
        r1 = conn.getresponse()  
        data1 = r1.read()
        json_decoder=JSONDecoder()
        conn.close()
        return json_decoder.decode(data1.decode())
    
    @staticmethod
    def gettrigerurl(servername,joburl):
        jobinfojson=JenkinsService.getjobinfo(servername,joburl.replace("http://"+servername,""))
        result=JenkinsService.getbuildparameters(jobinfojson)
        if len(result):
            joburl=joburl+"buildWithParameters?submitionid="
        return joburl
        
    
    @staticmethod
    def getbuildparameters(jobinfojson):
        parameters=list()
        actions=jobinfojson['actions']
        if len(actions):
            if actions[0].has_key('parameterDefinitions'):
                parameters=actions[0]['parameterDefinitions']
        result=list()
        if parameters:
            result=[parameter['name'] for parameter in parameters]
        return result
        
    
    @staticmethod
    def trigerbuild(jenkinserver,buildurl):
        JenkinsService.trigge_build_with_basic_auth(jenkinserver, buildurl)
#         conn = httplib2.HTTPConnectionWithTimeout(jenkinserver)
#         conn.request("POST",buildurl)
#         conn.getresponse() 
#         conn.close()

    
    @staticmethod
    def trigge_build_with_basic_auth(jenkinserver,buildurl):
        auth = base64.encodestring(('%s:%s' % ('admin','Perfect')).encode()).decode()[0:-1]
        headers = {"Authorization": "Basic "+ auth} 
        conn = httplib2.Http('.cache')
        conn.request(uri=buildurl,method="POST",headers=headers)
        


        
        
