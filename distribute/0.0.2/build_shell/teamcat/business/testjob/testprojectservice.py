#coding=utf-8
# coding=utf8
'''
Created on 2014-1-14
 
@author: zhangtiande
'''
from doraemon.testjob.models import TestProject
from dataaccess.testjob.dal_testproject import DAL_TestProject
from dataaccess.common.dal_user import DAL_User
from business.common.userservice import UserService

from gatesidelib.common.simplelogger import SimpleLogger


# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
 
class TestProjectService(object):
    '''
    business for Test testproject
    '''
     
    @staticmethod
    def vm_get_all_projects(request):
        try:
            pageindex = int(request.POST['pageindex'])
            searchkeyword = request.POST['searchkeyword']
            result = TestProjectService.gettestprojectbyfileter(searchkeyword).order_by("-id")
        except Exception as ex:
            SimpleLogger.error(ex)
        return result[12 * (pageindex - 1):12 * pageindex]
    
    @staticmethod
    def gettestprojectbygroup(user,testprojectqueyset):
        resultlist=list()
        try:
            
            if user.has_perm('testjob.view_all_testproject'):
                return testprojectqueyset
            for testproject in testprojectqueyset:
                for group in user.groups.all():
                    if testproject.TPSSubmiter!=None:
                        if group.name in TestProjectService.getsubmitorgroup(testproject.TPSSubmiter):
                            if testproject not in resultlist:
                                resultlist.append(testproject)
        except Exception as ex:
            SimpleLogger.error(ex)            
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
    def gettestprojectbyfileter(searchkeyword):
        if searchkeyword == "ALL":
                result = DAL_TestProject.get_all()
        else:
            result = TestProjectService.filtertestprojectbyid(searchkeyword)
            if result == None:
                result = TestProjectService.filtertestprojectbyname(searchkeyword)
        return result
    
    @staticmethod
    def get_testproject_pagecounts(request):
        searchkeyword=request.POST['searchkeyword']
        resultqueryset=TestProjectService.gettestprojectbyfileter(searchkeyword)
#         resultqueryset=TestProjectService.gettestprojectbygroup(request.user,resultqueryset)
        return len(resultqueryset)/12+1
     
    @staticmethod
    def filtertestprojectbyid(testprojectid):
        testproject = None
        try:
            testproject = DAL_TestProject.get_testproject(testprojectid)
        except Exception as ex:
            SimpleLogger.error(ex)
        return testproject
     
    @staticmethod
    def filtertestprojectbyname(testprojectname):
        result = None
        projectlist=list()
        try:
            for product in DAL_TestProject.get_all():
                if str(product.TPName).lower().count(testprojectname.lower())>0:
                    projectlist.append(product.id)
            result = DAL_TestProject.get_all().filter(id__in=projectlist)
        except Exception as ex:
            print(ex)
        return result
    
    @staticmethod
    def dm_createtestproject(request):
        ''' create new  db model testproject
        '''
        message = "successful"
        try:
            testproject = TestProject()
            testproject = TestProjectService.initlize_dm_instance(request, testproject)
            DAL_TestProject.add_testproject(testproject)
        except Exception as ex:
            SimpleLogger.error(ex)
        return message
         
             
                 
    @staticmethod
    def dm_updatetestproject(request):
        message = "successful"
        try:
            testprojectid = request.POST["testprojectid"]
            testproject = DAL_TestProject.get_testproject(testprojectid)
            testproject = TestProjectService.initlize_dm_instance(request,testproject)
            DAL_TestProject.add_testproject(testproject)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.error(ex)
        return message
    
    
    @staticmethod
    def dm_deletetestproject(request):
        message = "successful"
        try:
            testprojectid = request.POST["testprojectid"]
            testproject = DAL_TestProject.get_testproject(testprojectid)
            testproject.TPProjectIsActive=0
            DAL_TestProject.add_testproject(testproject)
        except Exception as ex:
            SimpleLogger.error(ex)
        return message
    
    
    
    
    @staticmethod
    def dm_copytestproject(requestpost):
        message = "successful"
        try:
            testprojectid = requestpost["testprojectid"]
            print(testprojectid)
            testproject = DAL_TestProject.get_testproject(testprojectid)
#             testproject.TPSStatus = TestJobStatusEnum.JobStatus_NotSubmit
            testproject.id=None
            testproject.TPSSubmitTime=None
            DAL_TestProject.add_testproject(testproject)
        except Exception as ex:
            SimpleLogger.error(ex)
        return message         
 


    @staticmethod
    def initlize_dm_instance(request, testproject):
        testproject = testproject
        testproject.TPName = request.POST.get("TPName")
        testproject.TPKEY = request.POST.get("TPKEY")
        testproject.TPProjectLead = request.POST.get("TPProjectLead")
        return testproject
             
     
    
    @staticmethod
    def get_testproject_lead(testprojectid):
        allusersList=[(user.id, user.last_name + user.first_name) for user in DAL_User.getallusers().order_by("id") if user.id>1]
        result=list()
        for user in allusersList:
            temp=dict()
            temp["text"]=user[1]
            temp["memberid"]=user[0]
            if testprojectid!=0:
                testproject=DAL_TestProject.get_testproject(testprojectid)
                if user[0] ==testproject.TPProjectLead:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    
    @staticmethod
    def get_testproject_key(testprojectid):
        result=""
        if testprojectid!=0:
            testproject = DAL_TestProject.get_testproject(testprojectid)
            result=testproject.TPKEY
        return result
    
    @staticmethod
    def get_testproject_name(testprojectid):
        result=""
        if testprojectid!=0:
            testproject = DAL_TestProject.get_testproject(testprojectid)
            result=testproject.TPName
        return result
    
    
    @staticmethod
    def init_testproject_form_control(request):
        result=""
        testprojectid=int(request.POST["testprojectid"])
        control_name=request.POST["controlname"]
        if control_name=="TESTPROJECTNAME":
            result=TestProjectService.get_testproject_name(testprojectid)
        
        if control_name=="TESTPROJECTKEY":
            result=TestProjectService.get_testproject_key(testprojectid)
            print(result)

        if control_name=="TESTPROJECTLEAD":
            result=TestProjectService.get_testproject_lead(testprojectid)
        
        
        return result
                
        
            
                
        
         
             
         
             
         
     
         
