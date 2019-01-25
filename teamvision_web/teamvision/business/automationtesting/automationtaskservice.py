#coding=utf-8
# coding=utf8
'''
Created on 2014-1-14
 
@author: zhangtiande
'''
from teamvision.automationtesting.models import AutoTask
from dataaccess.automationtesting.dal_automationtask import DAL_AutomationTask
from dataaccess.common.dal_user import DAL_User
from dataaccess.common.dal_dictvalue import DAL_DictValue
from dataaccess.automationtesting.dal_autotestconfig import DAL_AutoTestConfig
from dataaccess.automationtesting.dal_autoagent import DAL_AutoAgent
from dataaccess.automationtesting.dal_autotaskqueue import DAL_AutoTaskQueue
from gatesidelib.common.simplelogger import SimpleLogger
from teamvision.automationtesting.datamodels.automationtaskenum import AutomationTaskStatusEnum
from teamvision.automationtesting.datamodels.taskqueuecommandenum import AutoTaskQueueCommandTypeEnum
from teamvision.automationtesting.datamodels.autotaskqueuestatus import AutoTaskQueueStatusEnum
from teamvision.automationtesting.models import AutoTaskQueue



import time,uuid,socket

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
 
class AutomationTaskService(object):
    '''
    business for Test submition
    '''
     
    @staticmethod
    def vm_getalltasks(request):
        try:
            pageindex = int(request.POST['pageindex'])
            searchkeyword = request.POST['searchkeyword']
            result = AutomationTaskService.search_autotask(searchkeyword)
        except Exception as ex:
            print(ex)
        return result[15*(pageindex-1):15*pageindex]
    
    @staticmethod
    def get_autotask_page_counts(request):
        try:
            searchkeyword = request.POST['searchkeyword']
            result = AutomationTaskService.search_autotask(searchkeyword)
        except Exception as ex:
            print(ex)
        return len(result)/15+1
    
    @staticmethod
    def get_autotask_by_group(user,autotasklist):
        resultlist=list()
        if user.has_perm('autotask.view_all_autotask'):
            return autotasklist
        for autotask in autotasklist:
            if str(user.id) in eval(autotask.autotask.TJTester):
                resultlist.append(autotask)
        return resultlist
     
    @staticmethod
    def search_autotask(searchkeyword):
        if searchkeyword == "ALL":
            result = DAL_AutomationTask.get_all().filter(TaskIsActive=1)
        else:
            result = AutomationTaskService.search_autotask_byid(searchkeyword)
            if  result ==None or len(result)==0:
                result = AutomationTaskService.search_autotask_byname(searchkeyword.strip())
        return result.order_by("-id")
    
    @staticmethod
    def filterautotask(result,requestuser):
        result=AutomationTaskService.filter_autotask_submtion_type(result, requestuser)
        return result
    
    @staticmethod
    def filter_autotask_by_autotask_status(autotaskstatus,result):
        if autotaskstatus=="0":
            return result
        return result.filter(TJStatus=autotaskstatus)
        
    
        
     
    @staticmethod
    def search_autotask_byid(autotaskid):
        autotask = None
        try:
            autotask = DAL_AutomationTask.get_all().filter(id=autotaskid)
        except Exception as ex:
            SimpleLogger.error(ex.message)
        return autotask
     
    @staticmethod
    def search_autotask_byname(autotaskname):
        result = None
        try:
            result = DAL_AutomationTask.get_all().filter(TaskName__icontains=autotaskname)
        except Exception as ex:
            print(ex)
        return result
    
    @staticmethod
    def dm_createautotask(request):
        ''' create new  db model autotask
        '''
        message = "successful"
        try:
            autotask = AutoTask()
            autotask = AutomationTaskService.initlize_dm_instance(request,autotask)
            autotask.TaskStatus=AutomationTaskStatusEnum.TaskStatus_New
            DAL_AutomationTask.add_automationtask(autotask)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.error(message)
        return message
    
    
    @staticmethod
    def disable_autotask(request):
        
        message = "successful"
        try:
            autotask=DAL_AutomationTask.get_automation_task(request.POST["autotaskid"])
            autotask.TaskIsActive=0
            DAL_AutomationTask.add_automationtask(autotask)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.error(message)
        return message
    
    @staticmethod
    def copy_autotask(request):
        message = "successful"
        try:
            from_autotask=DAL_AutomationTask.get_automation_task(request.POST["autotaskid"])
            to_autotask=AutoTask()
            to_autotask.TaskAgentID=from_autotask.TaskAgentID
            to_autotask.TaskOwner=request.user.id
            to_autotask.TaskStatus=AutomationTaskStatusEnum.TaskStatus_New
            to_autotask.TaskCaseQuerySet=from_autotask.TaskCaseQuerySet
            to_autotask.TaskIsSplit=from_autotask.TaskIsSplit
            to_autotask.TaskName=from_autotask.TaskName+str(time.time())
            to_autotask.TaskProjectID=from_autotask.TaskProjectID
            to_autotask.TaskTestingConfigID=from_autotask.TaskTestingConfigID
#             to_autotask.TaskTpye=from_autotask.TaskTpye
            to_autotask.TaskViewScope=from_autotask.TaskViewScope
            DAL_AutomationTask.add_automationtask(to_autotask)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.error(message)
        return message
            
        
         
                   
    @staticmethod
    def dm_updateautotask(request):
        message = "successful"
        try:
            autotask=DAL_AutomationTask.get_automation_task(request.POST["autotaskid"])
            autotask = AutomationTaskService.initlize_dm_instance(request,autotask)
            DAL_AutomationTask.add_automationtask(autotask)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.error(message)
        return message
    
           
            
      
    @staticmethod
    def initlize_dm_instance(request, autotask):
        autotask.TaskName=request.POST.get("TaskName")
        autotask.TaskTestingConfigID=int(request.POST.get("TaskTestingConfigID"))
        autotask.TaskCaseQuerySet=int(request.POST.get("TaskCaseQuerySet"))
        autotask.TaskViewScope =int(request.POST.get("TaskViewScope"))
#         autotask.TaskTpye= request.POST.get("TaskTpye")
        autotask.TaskAgentID=int(request.POST.get("TaskAgentID"))
        autotask.TaskOwner=request.user.id
        autotask.TaskProjectID=int(request.POST.get("TaskProjectID"))
        autotask.TaskIsSplit=int(request.POST.get("TaskIsSplit"))
        return autotask
             
     
    @staticmethod
    def get_autotask_namelist():
        autotasklist = DAL_AutomationTask.get_all()
        return str([item.TaskName for item in autotasklist]).replace("u'","'")

     
    @staticmethod
    def get_autotask_types(autotaskid):
        tasktypes = DAL_DictValue.getdatavaluebytype("AutoTaskType")
        result=list()
        for tasktype in tasktypes:
            temp=dict()
            temp["text"]=tasktype.DicDataName
            temp["memberid"]=tasktype.DicDataValue
            if autotaskid!=0:
                autotask=DAL_AutomationTask.get_automation_task(autotaskid)
                if tasktype.DicDataValue==autotask.TaskTpye:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
     
    
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
    def get_autotask_name(autotaskid):
        result=""
        if autotaskid!=0:
            autotask=DAL_AutomationTask.get_automation_task(autotaskid)
            result=autotask.TaskName
        return result
    
    @staticmethod
    def get_autotask_testconfig(autotaskid,projectid):
        all_testingconfigs=DAL_AutoTestConfig.get_all_by_projectid(projectid)
        result=list()
        for testingconfig in all_testingconfigs:
            temp=dict()
            temp["text"]=testingconfig.TCFName
            temp["memberid"]=testingconfig.id
            print(autotaskid)
            if autotaskid!=0:
                autotask=DAL_AutomationTask.get_automation_task(autotaskid)
                if testingconfig.id==autotask.TaskTestingConfigID:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    
    @staticmethod
    def get_autotask_testcaseset(autotaskid):
        all_testingconfigs=DAL_AutoTestConfig.get_all()
        result=list()
        for testingconfig in all_testingconfigs:
            temp=dict()
            temp["text"]=testingconfig.TCFName
            temp["memberid"]=testingconfig.id
            if autotaskid!=0:
                autotask=DAL_AutomationTask.get_automation_task(autotaskid)
                if testingconfig.id==autotask.TaskTestingConfigID:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    
    @staticmethod
    def get_autotask_projests(autotaskid):
        all_projects=list()
        result=list()
        for project in all_projects:
            temp=dict()
            temp["text"]=project.TPName
            temp["memberid"]=project.id
            if autotaskid!=0:
                autotask=DAL_AutomationTask.get_automation_task(autotaskid)
                if project.id==autotask.TaskProjectID:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    @staticmethod
    def get_autotask_issplit(autotaskid):
        result=1
        if autotaskid!=0:
            autotask=DAL_AutomationTask.get_automation_task(autotaskid)
            result=autotask.TaskIsSplit
        return result
    
    @staticmethod
    def get_autotask_taskviewscope(autotaskid):
        result=1
        if autotaskid!=0:
            autotask=DAL_AutomationTask.get_automation_task(autotaskid)
            result=autotask.TaskViewScope
        return result
    
    @staticmethod
    def get_autotask_agent(autotaskid):
        all_agents=DAL_AutoAgent.get_all()
        result=list()
        for agent in all_agents:
            temp=dict()
            temp["text"]=agent.AName
            temp["memberid"]=agent.id
            if autotaskid!=0:
                autotask=DAL_AutomationTask.get_automation_task(autotaskid)
                if agent.id==autotask.TaskAgentID:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    

    @staticmethod
    def check_name_exits(request):
        auottaskname=request.POST["autotaskname"]
        return DAL_AutomationTask.taskname_exits(auottaskname)
    
    @staticmethod
    def init_autotask_form_control(request):
        result=""
        autotaskid=int(request.POST["autotaskid"])
        control_name=request.POST["controlname"]
        if control_name=="TASKTYPE":
            result=AutomationTaskService.get_autotask_types(autotaskid)
        
        if control_name=="TASKNAME":
            result=AutomationTaskService.get_autotask_name(autotaskid)

        if control_name=="TESTCONFIG":
            projectid=int(request.POST["projectid"])
            result=AutomationTaskService.get_autotask_testconfig(autotaskid,projectid)
            
        if control_name=="TESTCASE":
            result=AutomationTaskService.get_autotask_testcaseset(autotaskid)
            
        if control_name=="TASKPROJECT":
            result=AutomationTaskService.get_autotask_projests(autotaskid)
            
        if control_name=="TASKSPLIT":
            result=AutomationTaskService.get_autotask_issplit(autotaskid)
            
        if control_name=="TASKVIEWSCOPE":
            result=AutomationTaskService.get_autotask_taskviewscope(autotaskid)
            
        if control_name=="TASKAGENT":
            result=AutomationTaskService.get_autotask_agent(autotaskid)
        return result
    
    
    @staticmethod
    def start_task(autotaskid,triggername,fromip):
        autotask=DAL_AutomationTask.get_automation_task(autotaskid)
        autotask.TaskStatus=AutomationTaskStatusEnum.TaskStatus_Inqueue
        queuetask=AutoTaskQueue()
        queuetask.TQCommand=AutoTaskQueueCommandTypeEnum.TaskQueueCommandType_Start
        queuetask.TQPriority=2
        queuetask.TQStatus =AutoTaskQueueStatusEnum.QueueTaskStatus_New
        queuetask.TQTaskID=autotaskid
        queuetask.TQTaskUUID=uuid.uuid1()
        queuetask.TQFromName=triggername
        queuetask.TQFromIP=fromip
        DAL_AutoTaskQueue.add_task_inqueue(queuetask)
        DAL_AutomationTask.updatetask(autotask)
    
    @staticmethod
    def stop_task(autotaskid,triggername,fromip):
        queuetask=AutoTaskQueue()
        queuetask.TQCommand=AutoTaskQueueCommandTypeEnum.TaskQueueCommandType_Stop
        queuetask.TQPriority=7
        queuetask.TQStatus =AutoTaskQueueStatusEnum.QueueTaskStatus_New
        queuetask.TQTaskID=autotaskid
        queuetask.TQTaskUUID=uuid.uuid1()
        queuetask.TQFromName=triggername
        queuetask.TQFromIP=fromip
        DAL_AutoTaskQueue.add_task_inqueue(queuetask)
            
            
        
        
               
