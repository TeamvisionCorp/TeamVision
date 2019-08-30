#coding=utf-8
'''
Created on 2014-12-26

@author: zhangtiande
'''
from dataaccess.common.dal_dictvalue import DAL_DictValue
from dataaccess.testjob.dal_testsubmition import DAL_TestSubmition
from dataaccess.testjob.dal_codecommitlog import DAL_CodeCommitLog
from dataaccess.testjob.dal_testjob import DAL_TestJob
from dataaccess.testjob.dal_testproject import DAL_TestProject
from gatesidelib.common.simplelogger import  SimpleLogger


class CodeQualityService(object):
    '''
    business service for code quality
    '''


    @staticmethod
    def get_productname_control(platformid):
        SimpleLogger.logger.info("platform id"+str(platformid))
        joblist=DAL_TestJob.getall()
        result= "<option value=\"0\">请选择产品</option>"
        for job in joblist:
            submition=DAL_TestSubmition.gettestsubmition(job.TJSubmitionID)
            if submition:
                if submition.TPSPlatform==int(platformid):
                    dicdata=DAL_TestProject.get_testproject(submition.TPSProductName)
                    if dicdata.DicDataName not in result:
                        tempOption="<option value=\""+str(dicdata.id)+"\">"+dicdata.DicDataName+"</option>"
                        result=result+tempOption
        return result
    
    @staticmethod
    def get_productversion_control(productid,platformid):
        SimpleLogger.logger.info("platform id"+str(platformid))
        submitionList=DAL_TestSubmition.getproductversions(productid,platformid)
        result= "<option value=\"0\">请先选择产品</option>"
        for submition in submitionList:
            if submition.TPSProductVersion not in result and len(DAL_TestJob.getjobsbysubmitionid(submition.id)):
                tempOption="<option value=\""+str(submition.id)+"\">"+submition.TPSProductVersion+"</option>"
                result=result+tempOption
        return result
    
    @staticmethod
    def get_developer_newcodelines(submitionid):
        newcodelineslist=DAL_CodeCommitLog.get_developer_newcodelines(submitionid)
        developerlist=list()
        codelinescounts=list()
        for item in newcodelineslist:
            developerlist.append(item.get("CCLCommitor"))
            codelinescounts.append(item.get("NewCodeLines"))
        return str(developerlist).replace("u","")+";"+str(codelinescounts).replace("u","")
    
    @staticmethod
    def get_bugs_everyversion(submitionid):
        currentsubmition=DAL_TestSubmition.gettestsubmition(submitionid)
        resultdict=dict()
        if currentsubmition:
            submitionlist=DAL_TestSubmition.get_submition_by_productid(currentsubmition.TPSProductName,currentsubmition.TPSPlatform)
            for submition in submitionlist:
                testjobs=DAL_TestJob.getjobsbysubmitionid(submition.id)
                if len(testjobs):
                    if resultdict.has_key(submition.TPSProductVersion):
                        resultdict[submition.TPSProductVersion]=resultdict[submition.TPSProductVersion]+testjobs[0].TJBugCounts
                    else:
                        resultdict[submition.TPSProductVersion]=testjobs[0].TJBugCounts
        return CodeQualityService.generate_highchartdata(resultdict)
    
    @staticmethod
    def get_product_bugrates(submitionid):
        versionlist=list()
        bugrateslist=list()
        bugratesdata=CodeQualityService.generate_bugratesdata(submitionid)
        for k,v in zip(bugratesdata.iterkeys(),bugratesdata.itervalues()):
            versionlist.append(k)
            if  int(v[0])==0:
                bugrateslist.append(0)
            else:
                bugrateslist.append(round(v[1]*1000.0/v[0],2))
        versionlist.reverse()
        bugrateslist.reverse()
        return str(versionlist).replace("u","")+";"+str(bugrateslist).replace("u","")
    
    @staticmethod
    def generate_bugratesdata(submitionid):
        currentsubmition=DAL_TestSubmition.gettestsubmition(submitionid)
        resultdict=dict()
        if currentsubmition:
            submitionlist=DAL_TestSubmition.get_submition_by_productid(currentsubmition.TPSProductName,currentsubmition.TPSPlatform)
            for submition in submitionlist:
                testjobs=DAL_TestJob.getjobsbysubmitionid(submition.id)
                templist=list()
                if len(testjobs):
                    if testjobs[0].TJCodeLines==None:
                        codelines=0
                    else:
                        codelines=testjobs[0].TJCodeLines
                    if testjobs[0].TJBugCounts==None:
                        bugcounts=0
                    else:
                        bugcounts=testjobs[0].TJBugCounts
                    templist.append(int(codelines))
                    templist.append(bugcounts)
                    if resultdict.has_key(submition.TPSProductVersion):
                        templist[0]=templist[0]+resultdict[submition.TPSProductVersion][0]
                        templist[1]=templist[1]+resultdict[submition.TPSProductVersion][1]
                        resultdict[submition.TPSProductVersion]=templist
                    else:
                        resultdict[submition.TPSProductVersion]=templist
        return resultdict
        
    
    @staticmethod
    def generate_highchartdata(dictdata):
        keylist=list()
        valuelist=list()
        for k,v in zip(dictdata.iterkeys(),dictdata.itervalues()):
            keylist.append(k)
            valuelist.append(v)
        keylist.reverse()
        valuelist.reverse()
        return str(keylist).replace("u","")+";"+str(valuelist).replace("u","")
        
                
        
        
            
        
        