#coding=utf-8
# coding=utf8
'''
Created on 2014-1-14
 
@author: zhangtiande
'''
from doraemon.testjob.models import TestJob
from dataaccess.testjob.dal_testjob import DAL_TestJob
from doraemon.testjob.datamodels.testjobenum import TestJobStatusEnum
from dataaccess.common.dal_user import DAL_User
from dataaccess.common.dal_dictvalue import DAL_DictValue
from business.common.userservice import UserService
from business.common.emailservice import EmailService
from business.testjob.testsubmitionservice import TestSubmitionService
from dataaccess.testjob.dal_testsubmition import DAL_TestSubmition
from dataaccess.testjob.dal_projectversion import DAL_ProjectVersion
from doraemon.testjob.viewmodels.vm_testsubmition import VM_TestSubmition
from business.testjob.testjobhistoryservice import TestJobHistoryService
from gatesidelib.common.simplelogger import SimpleLogger


import datetime
from django.db.models import Q

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
 
class TestJobService(object):
    '''
    business for Test submition
    '''
     
    @staticmethod
    def vm_getalljobs(request):
        try:
            
            pageindex = int(request.POST['pageindex'])
            searchkeyword = request.POST['searchkeyword']
            result = TestJobService.searchjob(searchkeyword).order_by('-id')
            result=TestJobService.filterjob(result,request.user)
        except Exception as ex:
            print(ex)
        return TestJobService.getjobbygroup(request.user,result)[12 * (pageindex - 1):12 * pageindex]
    
    @staticmethod
    def getjobbygroup(user,joblist):
        resultlist=list()
        if user.has_perm('testjob.view_all_job'):
            return joblist
        for job in joblist:
            if "[" in job.TJTester:
                testlist=eval(job.TJTester.replace("[","").replace("']","").replace("u'","").replace("'","")+",")
            else:
                testlist=eval(job.TJTester)
            if user.id in testlist:
                resultlist.append(job)
        return resultlist
     
    @staticmethod
    def searchjob(searchkeyword):
        if searchkeyword == "ALL":
            result = DAL_TestJob.getall()
        else:
            result = TestJobService.searchjobbyid(searchkeyword)
            if  result ==None or len(result)==0:
                result = TestJobService.searchjobbyname(searchkeyword.strip())
        return result
    
    @staticmethod
    def filterjob(result,requestuser):
#         result=TestJobService.filter_job_by_job_status(result)
        result=TestJobService.filter_job_submtion_type(result, requestuser)
        return result
    
    @staticmethod
    def filter_job_by_job_status(jobstatus,result):
        if jobstatus=="0":
            return result
        return result.filter(TJStatus=jobstatus)
        
    
    @staticmethod
    def filter_job_submtion_type(result,requestuser):
        resultlist=list()
        if requestuser.has_perm('testjob.view_all_job'):
            return result
        for job in result:
            if "[" in job.TJTester:
                testlist=eval(job.TJTester.replace("[","").replace("']","").replace("u'","").replace("'","")+",")
            else:
                testlist=eval(job.TJTester)
            if requestuser.id in testlist:
                resultlist.append(job)
        return resultlist
        
     
    @staticmethod
    def searchjobbyid(jobid):
        job = None
        try:
            job = DAL_TestJob.getall().filter(id=jobid)
        except Exception as ex:
            SimpleLogger.logger.error(ex.message)
        return job
     
    @staticmethod
    def searchjobbyname(jobname):
        result = None
        try:
            result = DAL_TestJob.getall().filter(TJJobName__icontains=jobname)
        except Exception as ex:
            print(ex)
        return result
    
    @staticmethod
    def dm_createtestjob(request):
        ''' create new  db model testjob
        '''
        message = "successful"
        try:
            testjob = TestJob()
            testjob = TestJobService.initlize_dm_instance(request, testjob)
            testjob= TestJobService.dm_updatejobstatus(testjob)
            DAL_TestJob.addtestjob(testjob)
            TestJobService.sendjobemail(testjob.id)
            TestJobService.updatesubmitionstatus(testjob)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.logger.error(message)
        return message
         
                   
    @staticmethod
    def dm_updatejob(request):
        message = "successful"
        try:
            jobid = request.POST["testjobid"]
            testjob = DAL_TestJob.gettestjob(jobid)
            testjob = TestJobService.initlize_dm_instance(request,testjob)
            testjob= TestJobService.dm_updatejobstatus(testjob)
            DAL_TestJob.addtestjob(testjob)
            TestJobHistoryService.dm_addbuildhistory(testjob,request.user.id)
            TestJobService.updatesubmitionstatus(testjob)
        except Exception as ex:
            message=str(ex)
            SimpleLogger.logger.error(message)
        return message  
    
    @staticmethod
    def dm_updatejobstatus(testjob):
        datenow=str(datetime.date.today())
        if int(testjob.TJProgress)==0:
            if testjob.TJEndTime>=datenow:
                testjob.TJStatus=TestJobStatusEnum.JobStatus_Start
            else:
                testjob.TJStatus=TestJobStatusEnum.JobStatus_Delay
        if  int(testjob.TJProgress)>0 and int(testjob.TJProgress)<100:
            if testjob.TJEndTime>=datenow:
                testjob.TJStatus=TestJobStatusEnum.JobStatus_InTesting
            else:
                testjob.TJStatus=TestJobStatusEnum.JobStatus_Delay
        if int(testjob.TJProgress)==100 and (testjob.TJFinishedTime==None):
            testjob.TJFinishedTime=datenow
            if testjob.TJEndTime>=datenow:
                testjob.TJStatus=TestJobStatusEnum.JobStatus_Completed
            else:
                testjob.TJStatus=TestJobStatusEnum.JobStatus_Delay
        return testjob
    
    @staticmethod
    def updatesubmitionstatus(testjob):
        if str(testjob.TJStatus)==str(TestJobStatusEnum.JobStatus_Start):
            submition=TestSubmitionService.getsubmition(testjob.TJSubmitionID)
            if submition!=None and str(submition.TPSStatus)==str(TestJobStatusEnum.JobStatus_Submited):
                submition.TPSStatus=TestJobStatusEnum.JobStatus_Processed
                DAL_TestSubmition.updatesubmition(submition)
            
            

    @staticmethod
    def sendjobemail(jobid):
        job=TestJobService.getjob(jobid)
        submition=TestSubmitionService.getsubmition(job.TJSubmitionID)
        print("step1")
        if submition!=None:
            emaillist = TestJobService.getemaillist(job)
            print("step2")
            print(emaillist)
            emailconfig = TestJobService.getemaliconfig()
            summaryinfo="测试小伙伴已经对 项目：【" + job.TJJobName + "】做了测试安排！具体安排请看详细信息！"
            emailmessage = TestJobService.createemailmessage(job,summaryinfo,emailconfig['email_testjob_template'])
            subject ="项目：【" + job.TJJobName + "】做了测试安排！具体安排请看详细信息！" 
            EmailService.sendemail(emailconfig, emaillist, emailmessage, subject)
     
     
         
#     @staticmethod
#     def initlizetestjobformview(testjobid):
#         ''' create Testjob instance'''
#         if testjobid:
#             dm_job = TestJobService.getjob(testjobid)
#             dm_job.TJTester=eval(dm_job.TJTester)
#             customizeParameters = TestJobService.getformcustomizeparameters()
#             form = TestJobForm(customizeParameters, dm_job.__dict__)
#         else:
#             customizeParameters = TestJobService.getformcustomizeparameters()
#             form = TestJobForm(customizeParameters=customizeParameters)
             
#         return form
      
    @staticmethod
    def initlize_dm_instance(request, testjob):
        testjob.TJJobName=request.POST.get("TJJobName","")
        testjob.TJJobType=request.POST.get("TJJobType")
        testjob.TJSubmitionID=request.POST.get("TJSubmitionID")
        testjob.TJParentID = request.POST.get("TJParentID")
        testjob.TJStartTime= request.POST.get("TJStartTime")
        testjob.TJEndTime=request.POST.get("TJEndTime")
#         testjob.TJStatus=int(request.POST.get("TJStatus"))
        testjob.TJProgress=str(request.POST.get("TJProgress"))
        testjob.TJTester=str(request.POST.get("TJTester"))
        if  not testjob.TJTester:
            testjob.TJTester='0,0'
        if ',' not in testjob.TJTester:
            testjob.TJTester=testjob.TJTester+','
        testjob.TJJobType=request.POST.get("TJJobType")
        testjob.TJJobComments=request.POST.get("TJJobComments")
        testjob.TJBugCounts=request.POST.get("TJBugCounts")
        return testjob
             
     
    @staticmethod
    def getjob(jobid):
        testjob = DAL_TestJob.gettestjob(jobid)
        return testjob

     
    @staticmethod
    def get_job_types():
        avalibleprojecttypes = DAL_DictValue.getdatavaluebytype("JobType")
        return [(project.id, project.DicDataName) for project in avalibleprojecttypes]
     
    @staticmethod
    def get_jobs_status():
        allstatus = DAL_DictValue.getdatavaluebytype("JobStatus").filter(DicDataDesc=1)
#         allstatus=[(48,'暂停'),(50,'未来任务'),(51,'排队中')]
        return [(status.id, status.DicDataName) for status in allstatus]
    
    @staticmethod
    def get_all_testers():
        testers = DAL_User.getuserbygroup("QA")
        return [(tester.id, tester.last_name + tester.first_name) for tester in testers]
     

    @staticmethod
    def getdicvaluebyid(id):
        dicdata = DAL_DictValue.getdatavaluebyid(id)
        if dicdata:
            return dicdata.DicDataName
        else:
            return "--"
                 
     
    @staticmethod
    def getformcustomizeparameters():
        customizeParameters = {}
        customizeParameters['TJTester'] = TestJobService.get_all_testers()
        customizeParameters['TJStatus'] = TestJobService.get_jobs_status()
        customizeParameters['TJJobType'] = TestJobService.get_job_types()
        return customizeParameters;
     
    @staticmethod
    def getpostwapper(requestpost):
        postwapper = {}
        for (key, value)  in zip(requestpost.keys(), requestpost.values()):
            postwapper[key] = value
        return postwapper
         
    @staticmethod
    def getemaillist(job):
        submition=TestSubmitionService.getsubmition(job.TJSubmitionID)
        emaillist = TestJobService.getqaemaillist(submition.TPSProductType, [])
        emaillist = TestJobService.getccemaillist(submition.TPSCC, emaillist)
#         emaillist = TestJobService.getdevemaillist(emaillist)
        emaillist = TestJobService.getdefaultemailreciverlist(submition.TPSProductType,emaillist)
        submitoremail=UserService.getuser(submition.TPSSubmiter).email
        if submitoremail in emaillist:
            pass
        else:
            emaillist.append(submitoremail)
        print(emaillist)
        return emaillist
       
    @staticmethod
    def getccemaillist(ccids, outputemaillist):
        emaillist = outputemaillist
        if ccids != "0":
            for userid in eval(ccids):
                developer = UserService.getuser(userid)
                if developer !=None:
                    if developer.email in emaillist:
                        pass
                    else:
                        emaillist.append(developer.email)
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
    def getdevemaillist(submitorid,outputemaillist):
        emaillist=outputemaillist
        devgroups=UserService.getuser(submitorid).groups.all()
        for group in devgroups:
            for user in UserService.getusersbygroup(group.name):
                if user.has_perm('testjob.view_all_job'):
                    if user.email in emaillist:
                        pass
                    else:
                        emaillist.append(user.email)
        return emaillist
     
    @staticmethod
    def getdefaultemailreciverlist(producttypeid,outputemaillist):
        qagroup = DAL_DictValue.getdatavaluebyid(producttypeid).DicDataDesc
        emaillist = outputemaillist
        if qagroup!="DevTest":
            emailconfig = TestJobService.getemaliconfig()
            emailstring = emailconfig['defautrecivers']
            for email in emailstring.split(','):
                if email in emaillist:
                    pass
                else:
                    emaillist.append(email)
        return emaillist
         
         
     
    @staticmethod
    def createemailmessage(testjob, summaryinfo, emailtemplatepath):
        submition=TestSubmitionService.getsubmition(testjob.TJSubmitionID)
        emailtemplates = open(emailtemplatepath, 'rb').read()
        projectname = TestSubmitionService.getdicvaluebyid(submition.TPSProductName)
        platform = TestSubmitionService.getdicvaluebyid(submition.TPSPlatform)
        submitior = UserService.getuser(submition.TPSSubmiter)
        emailtemplates = emailtemplates.replace("${TESTJOBID}",str(testjob.id))
        emailtemplates = emailtemplates.replace("${SUBMITIONINFO}",summaryinfo)
        emailtemplates = emailtemplates.replace("${SUBMITTIME}", str(submition.TPSSubmitTime))
        emailtemplates = emailtemplates.replace("${SUBMITID}", str(submition.id))
        emailtemplates = emailtemplates.replace("${PROJECTNAME}", projectname)
        emailtemplates = emailtemplates.replace("${SUBMITIOR}", str(submitior.last_name + submitior.first_name))
        emailtemplates = emailtemplates.replace("${PLATFORM}", str(platform))
        emailtemplates = emailtemplates.replace("${VERSION}", TestJobService.get_project_version(submition))
        emailtemplates = emailtemplates.replace("${TESTERS}",str(TestJobService.get_job_tester(testjob)))
        emailtemplates = emailtemplates.replace("${STARTDATE}",str(testjob.TJStartTime))
        emailtemplates = emailtemplates.replace("${ENDDATE}",str(testjob.TJEndTime))
        return emailtemplates
     
    @staticmethod
    def getemaliconfig():
        result = {}
        allconfigs = DAL_DictValue.getdatavaluebytype("EmailConfig")
        for config in allconfigs:
            result[config.DicDataDesc] = config.DicDataName
        return result
    
    @staticmethod
    def get_job_tester(testjob):
        testnames=list()
        result=""
        if testjob.TJTester:
            testerlist=eval(testjob.TJTester)
            for testerid in testerlist:
                tester=UserService.getuser(testerid)
                testername=tester.last_name+tester.first_name
                if testername not in testnames:
                    result=result+testername+" "
        return result
    
    @staticmethod
    def get_job_name(request):
        if request.GET["submitionid"]!="0":
            submition=TestSubmitionService.getsubmition(request.GET["submitionid"])
            vm_submition=VM_TestSubmition(submition,request.user)
            jobname=vm_submition.getproductname()+"_"+TestJobService.get_project_version(submition)
        else:
            jobname=""
        return jobname
    
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
    def get_job_progress(request):
        job=TestJobService.getjob(request.GET['jobid'])
        normalprogress=0
        jobprogress=float(job.TJProgress)
        progresscolor='#fffffb' #白色
        datenow=datetime.date.today()
        if jobprogress==100:
            progresscolor="#a1a3a6"
        elif jobprogress==0:
            progresscolor='#fffffb'
        else:
            if job.TJStartTime<=datenow:
                normalprogress=(datenow-job.TJStartTime).days/((job.TJEndTime-job.TJStartTime).days*1.0+1)*100
                if (normalprogress-jobprogress)>20:
                    progresscolor='#ef4136' ##红色
                elif (normalprogress-jobprogress)<=20 and (normalprogress-jobprogress)>0:
                    progresscolor="#bed742" #黄色
                elif (jobprogress-normalprogress)>=0:
                    progresscolor='#1d953f' #绿色
        return str(jobprogress)[0:4].strip()+","+progresscolor
    
    
    @staticmethod
    def get_testjob_jobtypes(testjobid):
        avaliblejobtypes = DAL_DictValue.getdatavaluebytype("JobType")
        result=list()
        for dicdata in avaliblejobtypes:
            temp=dict()
            temp["text"]=dicdata.DicDataName
            temp["memberid"]=dicdata.id
            if testjobid!=0:
                testsubmition=DAL_TestJob.gettestjob(testjobid)
                if testsubmition.TJJobType==dicdata.id:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    @staticmethod
    def get_testjob_commitid(testjobid):
        result=""
        if testjobid!=0:
            testjob = DAL_TestJob.gettestjob(testjobid)
            result=testjob.TJSubmitionID
        return result
    
    @staticmethod
    def get_testjob_jobname(testjobid):
        result=""
        if testjobid!=0:
            testjob = DAL_TestJob.gettestjob(testjobid)
            result=testjob.TJJobName
        return result
    
    @staticmethod
    def get_testjob_starttime(testjobid):
        result=""
        if testjobid!=0:
            testjob = DAL_TestJob.gettestjob(testjobid)
            result=testjob.TJStartTime
        return result
    
    @staticmethod
    def get_testjob_endtime(testjobid):
        result=""
        if testjobid!=0:
            testjob = DAL_TestJob.gettestjob(testjobid)
            result=testjob.TJEndTime
        return result
    
    @staticmethod
    def get_testjob_bugcounts(testjobid):
        result=""
        if testjobid!=0:
            testjob = DAL_TestJob.gettestjob(testjobid)
            result=testjob.TJBugCounts
        return result
    
    @staticmethod
    def get_testjob_progress(testjobid):
        result=""
        if testjobid!=0:
            testjob = DAL_TestJob.gettestjob(testjobid)
            result=testjob.TJProgress
        return result
    
    
    @staticmethod
    def get_testjob_testers(testjobid):
        testers = DAL_User.getuserbygroup("QA")
        result=list()
        for tester in testers:
            temp=dict()
            temp["text"]=tester.last_name + tester.first_name
            temp["memberid"]=tester.id
            if testjobid!=0:
                testjob=DAL_TestJob.gettestjob(testjobid)
                if "[" in testjob.TJTester:
                    testerlist=eval(testjob.TJTester.replace("[","").replace("']","").replace("u'","").replace("'","")+",")
                else:
                    testerlist=eval(testjob.TJTester)
                if tester.id in testerlist:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    
    @staticmethod
    def get_testjob_status(testjobid):
        allstatus = DAL_DictValue.getdatavaluebytype("JobStatus").filter(DicDataDesc=1)
        result=list()
        for status in allstatus:
            temp=dict()
            temp["text"]=status.DicDataName
            temp["memberid"]=status.id
            if testjobid!=0:
                testjob=DAL_TestJob.gettestjob(testjobid)
                if status.id==testjob.TJStatus:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    
    
    @staticmethod
    def init_testjob_form_control(request):
        result=""
        testjobid=int(request.POST["testjobid"])
        control_name=request.POST["controlname"]
        if control_name=="TESTJOBTYPE":
            result=TestJobService.get_testjob_jobtypes(testjobid)
        
        if control_name=="TESTJOBCOMMITID":
            result=TestJobService.get_testjob_commitid(testjobid)
            
        if control_name=="TESTJOBNAME":
            result=TestJobService.get_testjob_jobname(testjobid)
            
        if control_name=="TESTJOBSTARTDATE":
            result=TestJobService.get_testjob_starttime(testjobid)
            
            
        if control_name=="TESTJOBENDDATE":
            result=TestJobService.get_testjob_endtime(testjobid)
            
        if control_name=="TESTJOBTESTER":
            result=TestJobService.get_testjob_testers(testjobid)
            
        if control_name=="TESTJOBSTATUS":
            result=TestJobService.get_testjob_status(testjobid)
        
        if control_name=="TESTJOBPROGRESS":
            result=TestJobService.get_testjob_progress(testjobid)
        
            
        if control_name=="TESTJOBBUGCOUNTS":
            result=TestJobService.get_testjob_bugcounts(testjobid)
        
        
        
        
        return result
        
             
         
             
         
     
         
