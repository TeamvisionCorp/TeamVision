#coding=utf-8
'''
Created on 2014-1-14
 
@author: zhangtiande
'''
from doraemon.testjob.models import TestProjectSubmition
from dataaccess.testjob.dal_testsubmition import DAL_TestSubmition
from dataaccess.testjob.dal_testproject import DAL_TestProject
from dataaccess.testjob.dal_projectversion import DAL_ProjectVersion
from doraemon.testjob.datamodels.testjobenum import TestJobStatusEnum
from dataaccess.common.dal_user import DAL_User
from dataaccess.common.dal_dictvalue import DAL_DictValue
from business.common.jenkinsservice import JenkinsService
from business.common.userservice import UserService
from gatesidelib.datetimehelper import DateTimeHelper
from gatesidelib.emailhelper import EmailHelper
from gatesidelib.common.simplelogger import SimpleLogger
from business.testjob.testbuildservice import TestBuildService
from dataaccess.testjob.dal_testjob import DAL_TestJob

import sys,imp
imp.reload(sys)
# sys.setdefaultencoding('utf-8')
 
class TestSubmitionService(object):
    '''
    business for Test submition
    '''
     
    @staticmethod
    def vm_getallsubmitions(request):
        try:
            pageindex = int(request.POST['pageindex'])
            searchkeyword = request.POST['searchkeyword'] 
            result = TestSubmitionService.getsubmitionbyfileter(searchkeyword).order_by("-id")
            result=TestSubmitionService.getsubmitionbygroup(request.user,result)
        except Exception as ex:
            print(ex)
        return result[12 * (pageindex - 1):12 * pageindex]
    
    @staticmethod
    def getsubmitionbygroup(user,submitionqueyset):
        resultlist=list()
        try:
            
            if user.has_perm('testjob.view_all_submition'):
                return submitionqueyset
            for submition in submitionqueyset:
                for group in user.groups.all():
                    if submition.TPSSubmiter!=None:
                        if group.name in TestSubmitionService.getsubmitorgroup(submition.TPSSubmiter):
                            if submition not in resultlist:
                                resultlist.append(submition)
        except Exception as ex:
            print(ex)
        return resultlist
    
    @staticmethod
    def getsubmitorgroup(submitorid):
        grouplist=list()
        user=UserService.getuser(submitorid)
        for group in user.groups.all():
            if group.name not in grouplist:
                grouplist.append(group.name)
        return grouplist
     
    @staticmethod
    def getsubmitionbyfileter(searchkeyword):
        if searchkeyword == "ALL":
                result = DAL_TestSubmition.getall()
        else:
            result = TestSubmitionService.filtersubmitionbyid(searchkeyword)
            if result == None:
                result = TestSubmitionService.filtersubmitionbyname(searchkeyword)
        return result
    
    @staticmethod
    def get_submition_pagecounts(request):
        searchkeyword=request.POST['searchkeyword']
        resultqueryset=TestSubmitionService.getsubmitionbyfileter(searchkeyword)
        resultqueryset=TestSubmitionService.getsubmitionbygroup(request.user,resultqueryset)
        return len(resultqueryset)/12+1
     
    @staticmethod
    def filtersubmitionbyid(submitionid):
        submition = None
        try:
            submition = DAL_TestSubmition.getall().filter(id=submitionid)
        except Exception as ex:
            print(ex)
        return submition
     
    @staticmethod
    def filtersubmitionbyname(submitionname):
        result = None
        projectlist=list()
        try:
            for product in DAL_TestProject.get_all():
                if str(product.DicDataName).lower().count(submitionname.lower())>0:
                    productdataid = product.id
                    projectlist.append(productdataid)
            result = DAL_TestSubmition.getall().filter(TPSProductName__in=projectlist)
        except Exception as ex:
            print(ex)
        return result
    @staticmethod
    def dm_createtestsubmition(request):
        ''' create new  db model testsubmition
        '''
        message = "successful"
        try:
            testsubmition = TestProjectSubmition()
            testsubmition = TestSubmitionService.initlize_dm_instance(request, testsubmition)
            testsubmition.TPSStatus = TestJobStatusEnum.JobStatus_NotSubmit
            testsubmition.TPSSubmiter =str(request.user.id)
            DAL_TestSubmition.addtestsubmition(testsubmition)
        except Exception as ex:
            message = str(ex)
        return message
         
             
                 
    @staticmethod
    def dm_updatesubmition(request):
        message = "successful"
        try:
            submitionid = request.POST["testsubmitionid"]
            testSubmition = DAL_TestSubmition.gettestsubmition(submitionid)
            testSubmition = TestSubmitionService.initlize_dm_instance(request, testSubmition)
            DAL_TestSubmition.addtestsubmition(testSubmition)
        except Exception as ex:
            message = str(ex)
            print(message)
        return message
    
    
    @staticmethod
    def dm_deletesubmition(request):
        message = "successful"
        try:
            submitionid = request.POST["testsubmitionid"]
            testsubmition = DAL_TestSubmition.gettestsubmition(submitionid)
            testsubmition.TPSIsActive=0
            DAL_TestSubmition.addtestsubmition(testsubmition)
        except Exception as ex:
            message = str(ex)
        return message
    
    
    
    
    @staticmethod
    def dm_copysubmition(requestpost):
        message = "successful"
        try:
            submitionid = requestpost["testsubmitionid"]
            print(submitionid)
            testsubmition = DAL_TestSubmition.gettestsubmition(submitionid)
            testsubmition.TPSStatus = TestJobStatusEnum.JobStatus_NotSubmit
            testsubmition.id=None
            testsubmition.TPSSubmitTime=None
            DAL_TestSubmition.addtestsubmition(testsubmition)
        except Exception as ex:
            message = str(ex)
        return message         
 
    @staticmethod
    def processsubmition(request):
        message = "successful"
        try:

            submitionid = request['testsubmitionid']
            testSubmition = DAL_TestSubmition.gettestsubmition(submitionid)
            emailconfig = TestSubmitionService.getemaliconfig()
            TestSubmitionService.sendsubmitionemail(submitionid, "已经提测了", "", "", emailconfig['emailsubmitiontemplatepath'])
            TestSubmitionService.updatesubmitiontime(submitionid)
            TestSubmitionService.trigerjenkinsjob(submitionid)
        except Exception as ex:
            print(ex)
            message = str(ex)
        return message
     
    @staticmethod
    def updatesubmitiontime(submitid):
        submitionid = submitid
        testSubmition = DAL_TestSubmition.gettestsubmition(submitionid)
        testSubmition.TPSSubmitTime = DateTimeHelper.getcnow()
        testSubmition.TPSStatus = TestJobStatusEnum.JobStatus_Submited
        DAL_TestSubmition.addtestsubmition(testSubmition)
         
     
    @staticmethod
    def processbuild(request):
        message = "successful"
        buildtitle="打包已经完成了！"
        try:
            submitionid = request["testsubmitionid"]
            emailconfig = TestSubmitionService.getemaliconfig()
            buildnumber = request['buildnumber']
            buildstatus = request['buildstatus']
            testSubmition = DAL_TestSubmition.gettestsubmition(submitionid)
            if not TestSubmitionService.is_job_finished(submitionid):
                TestSubmitionService.dm_updatesubmitionafterbuild(request)
            else:
                buildtitle="提测ID标示的产品已经测试完成，是不是打错包了！！！"
                message="打包已经完成，但该提测ID标示的产品已经测试完成，请检查提测ID"
            TestSubmitionService.sendsubmitionemail(submitionid, buildtitle, buildnumber,buildstatus,emailconfig['emailbuildtemplatepath'])
            TestSubmitionService.addbuildhistory(testSubmition, buildnumber, buildstatus)  
        except Exception as ex:
            message = str(ex)
        return message
    
    @staticmethod
    def addbuildhistory(testSubmition,buildnumber,buildstatus):
        if not TestSubmitionService.is_job_finished(testSubmition.id):
            buildurl=TestSubmitionService.getbuildurl(testSubmition.TPSJenkinsJobName,buildnumber)
            TestBuildService.dm_addbuildhistory(testSubmition,buildurl,buildstatus)
     
    @staticmethod
    def dm_updatesubmitionafterbuild(requestpost):
        message = "successful"
        try:
            submitionid = requestpost["testsubmitionid"]
            if not TestSubmitionService.is_job_finished(submitionid):
                testSubmition = DAL_TestSubmition.gettestsubmition(submitionid)
                testSubmition.TPSCodeVersion = requestpost["codeversion"]
                testSubmition.TPSPackageAddress = requestpost["packageurl"]
                testSubmition.TPSCodeUrl = requestpost["codeurl"]
                testSubmition.TPSCodeChangeLog=str(requestpost["change"]).decode('utf-8')[0:1000]
                DAL_TestSubmition.addtestsubmition(testSubmition)
        except Exception as ex:
            message = ex
        return message
 
    @staticmethod
    def sendsubmitionemail(submitionid, summaryinfo, buildno, buildstatus, emailtempaltepath):
        submition = TestSubmitionService.getsubmition(submitionid)
        emaillist = TestSubmitionService.getemaillist(submition)
        emailconfig = TestSubmitionService.getemaliconfig()
        emailmessage = TestSubmitionService.createemailmessage(submition, summaryinfo, buildstatus, buildno, emailtempaltepath)
        projectname = DAL_TestProject.get_testproject(submition.TPSProductName).TPName
        subject = "项目：【" + projectname + "】" + summaryinfo
        TestSubmitionService.sendemail(emailconfig, emaillist, emailmessage, subject)
     
    @staticmethod
    def sendemail(emailconfig, emaillist, emailmessage, subject):
        emailSender = EmailHelper(emailconfig['emailhost'], emailconfig['user'], emailconfig['password'], emailconfig['postfix'])
        for reciver in emaillist:
            index = 1
            message = emailSender.generatetextmessage(emailmessage, subject, ','.join(emaillist), 'html')
            emailSender.sendemaillogin(','.join(emaillist), subject, message.as_string())
            emaillist = emaillist[index:]
            emaillist.append(reciver)
     
         
#     @staticmethod
#     def initlizetestsubmitionformview(testsubmitionid):
#         ''' create TestProjectSubmition instance'''
#         if testsubmitionid:
#             dm_submition = TestSubmitionService.getsubmition(testsubmitionid)
#             dm_submition.TPSCC=eval(dm_submition.TPSCC)
#             customizeParameters = TestSubmitionService.getformcustomizeparameters(dm_submition.TPSJenkinsServer)
#             form = TestSubmitionForm(customizeParameters, dm_submition.__dict__)
#         else:
#             customizeParameters = TestSubmitionService.getformcustomizeparameters("")
#             form = TestSubmitionForm(customizeParameters=customizeParameters)
#              
#         return form
      
    @staticmethod
    def initlize_dm_instance(request, submition):
        testsubmition = submition
        testsubmition.TPSProductName = request.POST.get("TPSProductName")
        testsubmition.TPSProductType = request.POST.get("TPSProductType")
        testsubmition.TPSProductVersion = int(request.POST.get("TPSProductVersion"))
#         testsubmition.TPSDevelopers = str(request.POST.getlist("TPSDevelopers",[]))
        testsubmition.TPSCC = request.POST.get("TPSCC",'0,')
        if  not testsubmition.TPSCC:
            testsubmition.TPSCC='0,0'
        if ',' not in testsubmition.TPSCC:
            testsubmition.TPSCC=testsubmition.TPSCC+','
        testsubmition.TPSFunctionChange = request.POST.get("TPSFunctionChange").encode("utf8")[0:2000]
        testsubmition.TPSAdvice4Testing = request.POST.get("TPSAdvice4Testing").encode("utf8")
        testsubmition.TPSPlatform = request.POST.get("TPSPlatform")
        testsubmition.TPSJenkinsJobName = request.POST.get("TPSJenkinsJobName")
        testsubmition.TPSJenkinsServer = request.POST.get("TPSJenkinsServer")
#         testsubmition.TPSBugFix = request.POST.get("TPSBugFix").lstrip("<div>").rstrip("</div>")
        testsubmition.TPSBugFix = request.POST.get("TPSBugFix")
        testsubmition.TPSBuildParameters=request.POST.get("TPSBuildParameters")
        return testsubmition
             
     
    @staticmethod
    def getsubmition(submitionid):
        testsubmition = DAL_TestSubmition.gettestsubmition(submitionid)
        return testsubmition
 
    @staticmethod
    def getavalibleprojects():
        avalibleprojects = DAL_DictValue.getdatavaluebytype("ProjectName")
        return [(project.id, project.DicDataName) for project in avalibleprojects]
     
    @staticmethod
    def getprojecttypes():
        avalibleprojecttypes = DAL_DictValue.getdatavaluebytype("ProjectType")
        return [(project.id, project.DicDataName) for project in avalibleprojecttypes]
     
    @staticmethod
    def getsubmitionstatus():
        allstatus = DAL_DictValue.getdatavaluebytype("TestSubmitionStatus")
        return [(status.id, status.DicDataName) for status in allstatus]
     
    @staticmethod
    def getavalibleplatforms():
        allplatyforms = DAL_DictValue.getdatavaluebytype("TestPlatform")
        return [(platform.id, platform.DicDataName) for platform in allplatyforms]
     
    @staticmethod
    def getavaliblejenkinsservers():
        alljenkinsservers = DAL_DictValue.getdatavaluebytype("JenkinsServer")
        return [(jenkinsserver.id, jenkinsserver.DicDataDesc) for jenkinsserver in alljenkinsservers]
     
    @staticmethod
    def getavalibledevelopers():
        developers = DAL_User.getuserbygroup("Dev")
        return [(developer.id, developer.last_name + developer.first_name) for developer in developers]
     
     
    @staticmethod
    def getavaliblesubmitors():
        submitiors = DAL_User.getuserbygroup("Dev")
        return [(developer.id, developer.last_name + developer.first_name) for developer in submitiors]
     
    @staticmethod
    def getallusers():
        allusersList=[(user.id, user.last_name + user.first_name) for user in DAL_User.getallusers().order_by("username") if user.id > 1]
        return allusersList
    @staticmethod
    def getjenkinsjobs(serverid):
        servername=""
        if serverid:
            jenkinsserver = DAL_DictValue.getdatavaluebyid(serverid)
            servername=jenkinsserver.DicDataName
            jsonjobs = JenkinsService.getjenkinsjobs(servername)
        else:
            jenkinsservers = DAL_DictValue.getdatavaluebytype("JenkinsServer")
            servername=jenkinsservers[0].DicDataName
            jsonjobs = JenkinsService.getjenkinsjobs(servername)
        return [(job['url'], job['name']) for job in jsonjobs['jobs']]
         
     
    @staticmethod
    def getdicvaluebyid(id):
        dicdata = DAL_DictValue.getdatavaluebyid(id)
        if dicdata:
            return dicdata.DicDataName
        else:
            return "--"
                
     
    @staticmethod
    def getpostwapper(requestpost):
        postwapper = {}
        for (key, value)  in zip(requestpost.keys(), requestpost.values()):
            postwapper[key] = value
        return postwapper
     
    @staticmethod
    def getdevelopernames(developerids):
        names = []
        if developerids:
            for userid in eval(developerids):
                developer = UserService.getuser(userid)
                names.append(developer.username)
        return str(names)
         
    @staticmethod
    def getemaillist(submition):
        emaillist = TestSubmitionService.get_qa_email_list(submition, [])
        emaillist = TestSubmitionService.getccemaillist(submition.TPSCC, emaillist)
        emaillist = TestSubmitionService.get_dev_emaillist(submition,emaillist)
        emaillist = TestSubmitionService.get_pm_emaillist(submition,emaillist)
        emaillist = TestSubmitionService.getdefaultemailreciverlist(submition.TPSProductType,emaillist)
        submitoremail=UserService.getuser(submition.TPSSubmiter).email
        if submitoremail in emaillist:
            pass
        else:
            emaillist.append(submitoremail)
        return emaillist
       
    @staticmethod
    def getccemaillist(ccuserids, outputemaillist):
        emaillist = outputemaillist
        if ccuserids != "0":
            for userid in eval(ccuserids):
                ccuser = UserService.getuser(userid)
                if ccuser:
                    if ccuser.email in emaillist:
                        pass
                    else:
                        emaillist.append(ccuser.email)
        return emaillist
    
    
    @staticmethod
    def get_qa_email_list(testsubmition, outputemaillist):
        emaillist = outputemaillist
        try:
            if testsubmition.TPSProductVersion.isdigit():
                projectversion=DAL_ProjectVersion.get_projectversion(int(testsubmition.TPSProductVersion))
                if projectversion:
                    for testerid in eval(projectversion.PVTesters):
                        tester=UserService.getuser(testerid)
                        if tester.email in emaillist:
                            pass
                        else:
                            emaillist.append(tester.email)        
                else:
                    emaillist=TestSubmitionService.getqaemaillist(testsubmition.TPSProductType, outputemaillist)    
        except Exception as ex:
            print(ex)
        return emaillist
     
    @staticmethod
    def getqaemaillist(producttypeid, outputemaillist):
        qagroup = DAL_DictValue.getdatavaluebyid(producttypeid).DicDataDesc
        emaillist = outputemaillist
        for user in UserService.getusersbygroup(qagroup):
            if user.email in emaillist:
                pass
            else:
                emaillist.append(user.email)
        return emaillist
     
    @staticmethod
    def get_dev_emaillist(testsubmition,outputemaillist):
        emaillist = outputemaillist
        try:
            if testsubmition.TPSProductVersion.isdigit():
                projectversion=DAL_ProjectVersion.get_projectversion(int(testsubmition.TPSProductVersion))
                if projectversion:
                    for userid in eval(projectversion.PVDevelopers):
                        user=UserService.getuser(userid)
                        if user.email in emaillist:
                            pass
                        else:
                            emaillist.append(user.email)  
        except Exception as ex:
            print(ex)
        return emaillist
    
    @staticmethod
    def get_pm_emaillist(testsubmition,outputemaillist):
        emaillist = outputemaillist
        try:
            if testsubmition.TPSProductVersion.isdigit():
                projectversion=DAL_ProjectVersion.get_projectversion(int(testsubmition.TPSProductVersion))
                if projectversion:
                    for userid in eval(projectversion.PVPM):
                        user=UserService.getuser(userid)
                        if user.email in emaillist:
                            pass
                        else:
                            emaillist.append(user.email)  
        except Exception as ex:
            print(ex)
        return emaillist
    
     
    @staticmethod
    def getdefaultemailreciverlist(producttypeid,outputemaillist):
        qagroup = DAL_DictValue.getdatavaluebyid(producttypeid).DicDataDesc
        emaillist = outputemaillist
        if qagroup!="DevTest":
            emailconfig = TestSubmitionService.getemaliconfig()
            emailstring = emailconfig['defautrecivers']
            for email in emailstring.split(','):
                if email in emaillist:
                    pass
                else:
                    emaillist.append(email)
        return emaillist
         
     
    @staticmethod
    def getbuildurl(joburl, buildno):
        if buildno:
            return joburl + buildno
        else:
            return ""
     
    @staticmethod
    def getbuildlog(joburl, buildno):
        if buildno:
            return joburl + buildno + "/console"
        else:
            return ""
     
    @staticmethod
    def getbuildstatus(buildstatus):
        statusdicdata = DAL_DictValue.getdatavaluebytype("BuildStatus")
        for item in statusdicdata:
            if str(item.DicDataValue) == str(buildstatus):
                return item.DicDataName
         
     
    @staticmethod
    def createemailmessage(testsubmition, summaryinfo, buildstatus, buildno, emailtemplatepath):
        emailtemplates = open(emailtemplatepath, 'rb').read()
        projectname = DAL_TestProject.get_testproject(testsubmition.TPSProductName).TPName
        platform = TestSubmitionService.getdicvaluebyid(testsubmition.TPSPlatform)
        submitior = UserService.getuser(testsubmition.TPSSubmiter)
        emailtemplates = emailtemplates.replace("${SUBMITIONINFO}", "项目：【" + platform + projectname + TestSubmitionService.get_project_version(testsubmition)+ "】" + summaryinfo)
        emailtemplates = emailtemplates.replace("${SUBMITTIME}", str(DateTimeHelper.getcnow()))
        emailtemplates = emailtemplates.replace("${SUBMITID}", str(testsubmition.id))
        emailtemplates = emailtemplates.replace("${PROJECTNAME}", projectname)
        emailtemplates = emailtemplates.replace("${SUBMITIOR}", str(submitior.last_name + submitior.first_name))
        emailtemplates = emailtemplates.replace("${PLATFORM}", str(platform))
        emailtemplates = emailtemplates.replace("${VERSION}", TestSubmitionService.get_project_version(testsubmition))
        emailtemplates = emailtemplates.replace("${SVNVERSION}", str(testsubmition.TPSCodeVersion))
        emailtemplates = emailtemplates.replace("${SVNADDRESS}", str(testsubmition.TPSCodeUrl))
        emailtemplates = emailtemplates.replace("${FUNCTIONCHANGE}", str(testsubmition.TPSFunctionChange))
        emailtemplates = emailtemplates.replace("${BUGFIX}", str(testsubmition.TPSBugFix))
        emailtemplates = emailtemplates.replace("${SUGGESTION}", str(testsubmition.TPSAdvice4Testing))
        emailtemplates = emailtemplates.replace("${PACKAGEFORTESTING}", str(testsubmition.TPSPackageAddress))
        emailtemplates = emailtemplates.replace("${BUILDURL}", str(TestSubmitionService.getbuildurl(testsubmition.TPSJenkinsJobName, buildno)))
        emailtemplates = emailtemplates.replace("${BUILDLOGURL}", str(TestSubmitionService.getbuildlog(testsubmition.TPSJenkinsJobName, buildno)))
        emailtemplates = emailtemplates.replace("${BUILDSTATUS}", str(TestSubmitionService.getbuildstatus(buildstatus)))
        emailtemplates = emailtemplates.replace("${CODECHANGELOG}",TestSubmitionService.get_changelog(testsubmition.TPSCodeChangeLog))
        return emailtemplates
    
    @staticmethod
    def get_project_version(testsubmition):
        try:
            if testsubmition.TPSProductVersion.isdigit():
                projectversion=DAL_ProjectVersion.get_projectversion(int(testsubmition.TPSProductVersion))
                if projectversion:
                    return projectversion.PVVersion
                else:
                    return testsubmition.TPSProductVersion
            else:
                return testsubmition.TPSProductVersion
        except Exception as ex:
            print(ex)
     
    @staticmethod
    def getemaliconfig():
        result = {}
        allconfigs = DAL_DictValue.getdatavaluebytype("EmailConfig")
        for config in allconfigs:
            result[config.DicDataDesc] = config.DicDataName
        return result
     
    @staticmethod
    def getjenkinsjobshtml(request):
        jenkinsserverid = request.GET['id']
        jobs = TestSubmitionService.getjenkinsjobs(jenkinsserverid)
        jobshtml = ""
        for job in jobs:
            result = "<option value=\"" + job[0] + "\">" + job[1] + "</option>"
            jobshtml = jobshtml + result
        return str(jobshtml)
     
    @staticmethod
    def trigerjenkinsjob(submitionid):
        try:
            testSubmition = DAL_TestSubmition.gettestsubmition(submitionid)
            jenkinsserver = DAL_DictValue.getdatavaluebyid(testSubmition.TPSJenkinsServer).DicDataName
            joburl = testSubmition.TPSJenkinsJobName.replace("http://" + jenkinsserver, '')
            joburl =joburl.replace("job",'mpttrigger')
            urllist=joburl.split('/')
            newurl="/"+urllist[1]+"/"+urllist[2]+"/build?mptjob="+urllist[3]+"&mptid="+str(submitionid)+"&"+testSubmition.TPSBuildParameters
            JenkinsService.trigerbuild(jenkinsserver, str(newurl).strip())
        except Exception as ex:
            pass
            
        
    
    @staticmethod
    def is_job_finished(submitionid):
        result=False
        try:
            testjobs=DAL_TestJob.getjobsbysubmitionid(submitionid)
            if len(testjobs):
                result= testjobs[0].TJProgress=='100'
            else:
                result= False
        except Exception as ex:
            print(ex)
        return result
    
    @staticmethod
    def get_changelog(sourcelogs):
        result=""
        if sourcelogs:
            logs=sourcelogs.split("[##]")
            for log in logs:
                result=result+"<div>"+log+"</div>"
        return result
    
    @staticmethod
    def get_testsubmition_platforms(testsubmitionid):
        allplatforms = DAL_DictValue.getdatavaluebytype("TestPlatform")
        result=list()
        for dicdata in allplatforms:
            temp=dict()
            temp["text"]=dicdata.DicDataName
            temp["memberid"]=dicdata.id
            if testsubmitionid!=0:
                testsubmition=DAL_TestSubmition.gettestsubmition(testsubmitionid)
                if testsubmition.TPSPlatform==dicdata.id:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    @staticmethod
    def get_testsubmition_projecttype(testsubmitionid):
        avalibleprojecttypes = DAL_DictValue.getdatavaluebytype("ProjectType")
        result=list()
        for dicdata in avalibleprojecttypes:
            temp=dict()
            temp["text"]=dicdata.DicDataName
            temp["memberid"]=dicdata.id
            if testsubmitionid!=0:
                testsubmition=DAL_TestSubmition.gettestsubmition(testsubmitionid)
                if testsubmition.TPSProductType==dicdata.id:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    
    
    @staticmethod
    def get_testsubmition_testproject(testsubmitionid):
        avalibleprojects=DAL_TestProject.get_all()
        result=list()
        for project in avalibleprojects:
            temp=dict()
            temp["text"]=project.TPName
            temp["memberid"]=project.id
            if testsubmitionid!=0:
                testsubmition=DAL_TestSubmition.gettestsubmition(testsubmitionid)
                if testsubmition.TPSProductName==project.id:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    @staticmethod
    def getsubmition_jenkinsserver(testsubmitionid):
        alljenkinsservers = DAL_DictValue.getdatavaluebytype("JenkinsServer")
        result=list()
        for dicdata in alljenkinsservers:
            temp=dict()
            temp["text"]=dicdata.DicDataName
            temp["memberid"]=dicdata.id
            if testsubmitionid!=0:
                testsubmition=DAL_TestSubmition.gettestsubmition(testsubmitionid)
                if testsubmition.TPSJenkinsServer==dicdata.id:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    @staticmethod
    def getsubmition_jenkinsjobs(testsubmitionid,jenkinsserverid):
        if jenkinsserverid:
            jenkinsserver = DAL_DictValue.getdatavaluebyid(jenkinsserverid)
            servername=jenkinsserver.DicDataName
            jsonjobs = JenkinsService.getjenkinsjobs(servername)
        else:
            jenkinsservers = DAL_DictValue.getdatavaluebytype("JenkinsServer")
            servername=jenkinsservers[0].DicDataName
            jsonjobs = JenkinsService.getjenkinsjobs(servername)
        result=list()
        for job in jsonjobs['jobs']:
            temp=dict()
            temp["text"]=job['name']
            temp["memberid"]=job['url']
            if testsubmitionid!=0:
                testsubmition=DAL_TestSubmition.gettestsubmition(testsubmitionid)
                if testsubmition.TPSJenkinsJobName==job['url']:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    @staticmethod
    def getsubmition_all_emaillist(testsubmitionid):
        allusersList=[(user.id, user.last_name + user.first_name) for user in DAL_User.getallusers().order_by("id") if user.id>1]
        result=list()
        for user in allusersList:
            temp=dict()
            temp["text"]=user[1]
            temp["memberid"]=user[0]
            if testsubmitionid!=0:
                testsubmition=DAL_TestSubmition.gettestsubmition(testsubmitionid)
                if user[0] in eval(testsubmition.TPSCC):
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    
    
    
    @staticmethod
    def getsubmition_version(testsubmitionid,projectid):
        avalible_version=DAL_ProjectVersion.get_project_version(projectid)
        result=list()
        for version in avalible_version:
            temp=dict()
            temp["text"]=version.PVVersion
            temp["memberid"]=version.id
            if testsubmitionid!=0:
                testsubmition=DAL_TestSubmition.gettestsubmition(testsubmitionid)
                if int(testsubmition.TPSProductVersion)==version.id:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    @staticmethod
    def getsubmition_newfeature(submitionid):
        result=""
        if submitionid!=0:
            testsubmition = DAL_TestSubmition.gettestsubmition(submitionid)
            result=testsubmition.TPSFunctionChange
        return result
    
    @staticmethod
    def getsubmition_bugfix(submitionid):
        result=""
        if submitionid!=0:
            testsubmition = DAL_TestSubmition.gettestsubmition(submitionid)
            result=testsubmition.TPSBugFix
        return result
    
    @staticmethod
    def getsubmition_advance(submitionid):
        result=""
        if submitionid!=0:
            testsubmition = DAL_TestSubmition.gettestsubmition(submitionid)
            result=testsubmition.TPSAdvice4Testing
        return result
    
    @staticmethod
    def getsubmition_build_parameter(submitionid):
        result=""
        if submitionid!=0:
            testsubmition = DAL_TestSubmition.gettestsubmition(submitionid)
            result=testsubmition.TPSBuildParameters
        return result
    
    
    @staticmethod
    def init_testsubmition_form_control(request):
        result=""
        testsubmitionid=int(request.POST["testsubmitionid"])
        print(testsubmitionid)
        control_name=request.POST["controlname"]
        if control_name=="TESTSUBMITIONPLATFORM":
            result=TestSubmitionService.get_testsubmition_platforms(testsubmitionid)
        
        if control_name=="TESTSUBMITIONPROJECTTYPE":
            result=TestSubmitionService.get_testsubmition_projecttype(testsubmitionid)

        if control_name=="TESTPROJECT":
            result=TestSubmitionService.get_testsubmition_testproject(testsubmitionid)
            
        if control_name=="TESTSUBMITIONPROJECTVERSION":
            projectid=int(request.POST["projectid"])
            result=TestSubmitionService.getsubmition_version(testsubmitionid,projectid)
            print(result)
            
            
        if control_name=="TESTSUBMITIONNEWFEATURE":
            result=TestSubmitionService.getsubmition_newfeature(testsubmitionid)
            
        if control_name=="TESTSUBMITIONBUGFIX":
            result=TestSubmitionService.getsubmition_bugfix(testsubmitionid)
            
        if control_name=="TESTSUBMITIONADVANCE":
            result=TestSubmitionService.getsubmition_advance(testsubmitionid)
        
        if control_name=="TPSJENKINSSERVER":
            result=TestSubmitionService.getsubmition_jenkinsserver(testsubmitionid)
        
        if control_name=="TPSJENKINSJOB":
            jenkinsserverid=int(request.POST["jenkinsserverid"])
            result=TestSubmitionService.getsubmition_jenkinsjobs(testsubmitionid,jenkinsserverid)
        
        if control_name=="TPSCC":
            result=TestSubmitionService.getsubmition_all_emaillist(testsubmitionid)
            
        if control_name=="TPSBUILDPARAMETER":
            result=TestSubmitionService.getsubmition_build_parameter(testsubmitionid)
        
        
        return result
    
    @staticmethod
    def check_version_exits(productversion):
        return DAL_TestSubmition.get_submition_byversion(productversion)
                
        
            
                
        
         
             
         
             
         
     
         
