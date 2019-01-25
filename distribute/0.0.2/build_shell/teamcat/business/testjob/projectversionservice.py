#coding=utf-8
# coding=utf8
'''
Created on 2014-1-14
 
@author: zhangtiande
'''
from doraemon.testjob.models import ProjectVersion
from dataaccess.testjob.dal_projectversion import DAL_ProjectVersion
from dataaccess.testjob.dal_testproject import DAL_TestProject
from dataaccess.common.dal_user import DAL_User
from business.common.userservice import UserService

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
 
class ProjectVersionService(object):
    '''
    business for Test projectversion
    '''
     
    @staticmethod
    def vm_get_all_projects(request):
        try:
            pageindex = int(request.POST['pageindex'])
            projectid=request.POST["projectid"]
            result = DAL_ProjectVersion.get_all().filter(PVProjectID=int(projectid))
        except Exception as ex:
            print(ex)
        return result[12 * (pageindex - 1):12 * pageindex]
    
    @staticmethod
    def get_projectversion_pagecounts(request):
        pagecounts=1
        try:
            pageindex = int(request.POST['pageindex'])
            projectid=request.POST["projectid"]
            result = DAL_ProjectVersion.get_all().filter(PVProjectID=int(projectid))
            if len(result):
                pagecounts=len(result)/12+1
        except Exception as ex:
            print(ex)
        return pagecounts
        
    
    
    @staticmethod
    def dm_create_projectversion(request):
        ''' create new  db model projectversion
        '''
        message = "successful"
        try:
            projectversion = ProjectVersion()
            projectversion = ProjectVersionService.initlize_dm_instance(request, projectversion)
            DAL_ProjectVersion.add_projectversion(projectversion)
        except Exception as ex:
            message = str(ex)
        return message
         
             
                 
    @staticmethod
    def dm_update_projectversion(request):
        message = "successful"
        try:
            projectversionid = request.POST["projectversionid"]
            projectversion = DAL_ProjectVersion.get_projectversion(projectversionid)
            projectversion = ProjectVersionService.initlize_dm_instance(request,projectversion)
            DAL_ProjectVersion.add_projectversion(projectversion)
        except Exception as ex:
            message = str(ex)
            print(message)
        return message
    
    
    @staticmethod
    def dm_delete_projectversion(request):
        message = "successful"
        try:
            projectversionid = request.POST["projectversionid"]
            print(projectversionid)
            projectversion = DAL_ProjectVersion.get_projectversion(projectversionid)
            projectversion.TPProjectIsActive=0
            DAL_ProjectVersion.add_projectversion(projectversion)
        except Exception as ex:
            message = str(ex)
        return message
    
    
    
    
    @staticmethod
    def dm_copy_projectversion(requestpost):
        message = "successful"
        try:
            projectversionid = requestpost["projectversionid"]
            projectversion = DAL_ProjectVersion.get_projectversion(projectversionid)
#             projectversion.TPSStatus = TestJobStatusEnum.JobStatus_NotSubmit
            projectversion.id=None
            projectversion.TPSSubmitTime=None
            DAL_ProjectVersion.add_projectversion(projectversion)
        except Exception as ex:
            message = str(ex)
        return message         


      
    @staticmethod
    def initlize_dm_instance(request, projectversion):
        projectversion.PVProjectID = request.POST.get("PVProjectID")
        projectversion.PVVersion = request.POST.get("PVVersion")
        projectversion.PVTesters = request.POST.get("PVTesters","0,")
        if  not projectversion.PVTesters:
            projectversion.PVTesters='0,0'
        if ',' not in projectversion.PVTesters:
            projectversion.PVTesters=projectversion.PVTesters+','
        projectversion.PVDevelopers=request.POST.get("PVDevelopers")
        if  not projectversion.PVDevelopers:
            projectversion.PVDevelopers='0,0'
        if ',' not in projectversion.PVDevelopers:
            projectversion.PVDevelopers=projectversion.PVDevelopers+','
        projectversion.PVPM=request.POST.get("PVPM")
        if  not projectversion.PVPM:
            projectversion.PVPM='0,0'
        if ',' not in projectversion.PVPM:
            projectversion.PVPM=projectversion.PVPM+','
        return projectversion
             
     
    
    @staticmethod
    def get_projectversion_testers(projectversionid):
        allusersList=[(user.id, user.last_name + user.first_name) for user in DAL_User.getallusers().order_by("id") if user.id>1]
        result=list()
        for user in allusersList:
            temp=dict()
            temp["text"]=user[1]
            temp["memberid"]=user[0]
            if projectversionid!=0:
                projectversion=DAL_ProjectVersion.get_projectversion(projectversionid)
                if user[0] in eval(projectversion.PVTesters):
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    @staticmethod
    def get_projectversion_developers(projectversionid):
        allusersList=[(user.id, user.last_name + user.first_name) for user in DAL_User.getallusers().order_by("id") if user.id>1]
        result=list()
        for user in allusersList:
            temp=dict()
            temp["text"]=user[1]
            temp["memberid"]=user[0]
            if projectversionid!=0:
                projectversion=DAL_ProjectVersion.get_projectversion(projectversionid)
                if user[0] ==user[0] in eval(projectversion.PVDevelopers):
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")

    @staticmethod
    def get_projectversion_pms(projectversionid):
        allusersList=[(user.id, user.last_name + user.first_name) for user in DAL_User.getallusers().order_by("id") if user.id>1]
        result=list()
        for user in allusersList:
            temp=dict()
            temp["text"]=user[1]
            temp["memberid"]=user[0]
            if projectversionid!=0:
                projectversion=DAL_ProjectVersion.get_projectversion(projectversionid)
                if user[0] in eval(projectversion.PVPM):
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    @staticmethod
    def get_projectversion_project(projectversionid):
        alltestprojects=DAL_TestProject.get_all()
        result=list()
        for project in alltestprojects:
            temp=dict()
            temp["text"]=project.TPName
            temp["memberid"]=project.id
            if projectversionid!=0:
                projectversion=DAL_ProjectVersion.get_projectversion(projectversionid)
                if project.id ==projectversion.PVProjectID:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    @staticmethod
    def get_projectversion_version(projectversionid):
        result=""
        if projectversionid!=0:
            projectversion = DAL_ProjectVersion.get_projectversion(projectversionid)
            result=projectversion.PVVersion
        return result
    
    
    @staticmethod
    def init_projectversion_form_control(request):
        result=""
        projectversionid=int(request.POST["projectversionid"])
        control_name=request.POST["controlname"]
        if control_name=="PVPROJECT":
            result=ProjectVersionService.get_projectversion_project(projectversionid)
        
        if control_name=="PVVERSION":
            result=ProjectVersionService.get_projectversion_version(projectversionid)
            print(result)

        if control_name=="PVTESTERS":
            result=ProjectVersionService.get_projectversion_testers(projectversionid)
        
        if control_name=="PVDEVELOPERS":
            result=ProjectVersionService.get_projectversion_developers(projectversionid)
        
        if control_name=="PVPMS":
            result=ProjectVersionService.get_projectversion_pms(projectversionid)
        
        
        return result
    
                
        
            
                
        
         
             
         
             
         
     
         
