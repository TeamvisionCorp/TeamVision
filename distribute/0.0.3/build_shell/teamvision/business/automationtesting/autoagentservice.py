#coding=utf-8
# coding=utf8
'''
Created on 2014-1-14
 
@author: zhangtiande
'''
from teamvision.automationtesting.models import AutoAgent
from dataaccess.automationtesting.dal_autoagent import DAL_AutoAgent
from dataaccess.common.dal_user import DAL_User
from dataaccess.common.dal_dictvalue import DAL_DictValue
from gatesidelib.common.simplelogger import SimpleLogger
from teamvision.automationtesting.datamodels.autoagentenum import AutoAgentStatusEnum


import time

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
 
class AutoAgentService(object):
    '''
    business for Test submition
    '''
     
    @staticmethod
    def vm_getall_auotagent(request):
        try:
            pageindex = int(request.POST['pageindex'])
            searchkeyword = request.POST['searchkeyword']
            result = AutoAgentService.search_autoagent(searchkeyword)
        except Exception as ex:
            print(ex)
        return result[15*(pageindex-1):15*pageindex]
    
    @staticmethod
    def get_autoagent_page_counts(request):
        try:
            searchkeyword = request.POST['searchkeyword']
            result = AutoAgentService.search_autoagent(searchkeyword)
        except Exception as ex:
            print(ex)
        return len(result)/15+1
    
    @staticmethod
    def get_autoagent_by_group(user,autoagentlist):
        resultlist=list()
        if user.has_perm('autoagent.view_all_autoagent'):
            return autoagentlist
        for autoagent in autoagentlist:
            if str(user.id) in eval(autoagent.autoagent.TJTester):
                resultlist.append(autoagent)
        return resultlist
     
    @staticmethod
    def search_autoagent(searchkeyword):
        if searchkeyword == "ALL":
            result = DAL_AutoAgent.get_all().filter(AIsActive=1)
        else:
            result = AutoAgentService.search_autoagent_byid(searchkeyword)
            if  result ==None or len(result)==0:
                result = AutoAgentService.search_autoagent_byname(searchkeyword.strip())
        return result.order_by("-id")
    
    @staticmethod
    def filterautoagent(result,requestuser):
        result=AutoAgentService.filter_autoagent_submtion_type(result, requestuser)
        return result
    
    @staticmethod
    def filter_autoagent_by_autoagent_status(autoagentstatus,result):
        if autoagentstatus=="0":
            return result
        return result.filter(TJStatus=autoagentstatus)
        
    
        
     
    @staticmethod
    def search_autoagent_byid(autoagentid):
        autoagent = None
        try:
            autoagent = DAL_AutoAgent.get_all().filter(id=autoagentid)
        except Exception as ex:
            SimpleLogger.error(ex.message)
        return autoagent
     
    @staticmethod
    def search_autoagent_byname(autoagentname):
        result = None
        try:
            result = DAL_AutoAgent.get_all().filter(AName__icontains=autoagentname)
        except Exception as ex:
            print(ex)
        return result
    
    @staticmethod
    def dm_createautoagent(request):
        ''' create new  db model autoagent
        '''
        message = "successful"
        try:
            autoagent = AutoAgent()
            autoagent = AutoAgentService.initlize_dm_instance(request,autoagent)
            DAL_AutoAgent.add_autoagent(autoagent)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.error(message)
        return message
    
    
    @staticmethod
    def disable_autoagent(request):
        
        message = "successful"
        try:
            autoagent=DAL_AutoAgent.get_autoagent(request.POST["autoagentid"])
            autoagent.TaskIsActive=0
            DAL_AutoAgent.add_autoagent(autoagent)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.error(message)
        return message
    
    @staticmethod
    def copy_autoagent(request):
        message = "successful"
        try:
            from_autoagent=DAL_AutoAgent.get_autoagent(request.POST["autoagentid"])
            to_autoagent=AutoAgent()
            to_autoagent.AName=from_autoagent.AName
            to_autoagent.AOS=from_autoagent.AOS
            to_autoagent.AIP=from_autoagent.AIP
            to_autoagent.AStatus=AutoAgentStatusEnum.AgentStatus_Offline
            to_autoagent.AAgentBrowser=from_autoagent.AAgentBrowser
            to_autoagent.AIsReserved=from_autoagent.AIsReserved
            DAL_AutoAgent.add_autoagent(to_autoagent)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.error(message)
        return message
            
        
         
                   
    @staticmethod
    def dm_updateautoagent(request):
        message = "successful"
        try:
            autoagent=DAL_AutoAgent.get_autoagent(request.POST["autoagentid"])
            autoagent = AutoAgentService.initlize_dm_instance(request,autoagent)
            DAL_AutoAgent.add_autoagent(autoagent)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.error(message)
        return message
    
           
            
      
    @staticmethod
    def initlize_dm_instance(request, autoagent):
        
        autoagent.AName=request.POST.get("AName")
        autoagent.AOS=int(request.POST.get("AOS"))
        autoagent.AIP=request.POST.get("AIP")
        autoagent.AAgentBrowser = request.POST.get("AAgentBrowser")
        if ',' not in autoagent.AAgentBrowser:
            autoagent.AAgentBrowser=autoagent.AAgentBrowser+","
        autoagent.AStatus=AutoAgentStatusEnum.AgentStatus_Offline
        autoagent.AIsReserved=int(request.POST.get("AIsReserved"))
        autoagent.AAgentWorkSpace=request.POST.get("AAgentWorkSpace")
        return autoagent
             
     
    @staticmethod
    def get_autoagent_namelist():
        autoagentlist = DAL_AutoAgent.get_all()
        return str([item.TaskName for item in autoagentlist]).replace("u'","'")

     
    @staticmethod
    def get_autoagent_types(autoagentid):
        tasktypes = DAL_DictValue.getdatavaluebytype("AutoTaskType")
        result=list()
        for tasktype in tasktypes:
            temp=dict()
            temp["text"]=tasktype.DicDataName
            temp["memberid"]=tasktype.DicDataValue
            if autoagentid!=0:
                autoagent=DAL_AutoAgent.get_autoagent(autoagentid)
                if tasktype.DicDataValue==autoagent.TaskTpye:
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
    def get_autoagent_name(autoagentid):
        result=""
        if autoagentid!=0:
            autoagent=DAL_AutoAgent.get_autoagent(autoagentid)
            result=autoagent.AName
        return result
    
    @staticmethod
    def get_autoagent_os(autoagentid):
        all_os=DAL_DictValue.getdatavaluebytype("AgentOSType")
        result=list()
        if autoagentid!=0:
            autoagent=DAL_AutoAgent.get_autoagent(autoagentid)
        for os in all_os:
            temp=dict()
            temp["text"]=os.DicDataName
            temp["memberid"]=os.DicDataValue
            if autoagentid!=0:
                if os.DicDataValue==autoagent.AOS:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    
    
    @staticmethod
    def get_autoagent_browsers(autoagentid):
        all_browsers=DAL_DictValue.getdatavaluebytype("AutoTaskRuntime").filter(DicDataDesc='WEB')
        result=list()
        if autoagentid!=0:
            autoagent=DAL_AutoAgent.get_autoagent(autoagentid)
        for browser in all_browsers:
            temp=dict()
            temp["text"]=browser.DicDataName
            temp["memberid"]=browser.DicDataValue
            if autoagentid!=0:
                if browser.DicDataValue in eval(autoagent.AAgentBrowser):
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    @staticmethod
    def get_autoagent_ip(autoagentid):
        result=""
        if autoagentid!=0:
            autoagent=DAL_AutoAgent.get_autoagent(autoagentid)
            result=autoagent.AIP
        return result
    
    @staticmethod
    def get_autoagent_reserved(autoagentid):
        result=1
        if autoagentid!=0:
            autoagent=DAL_AutoAgent.get_autoagent(autoagentid)
            result=autoagent.AIsReserved
        return result
    
    @staticmethod
    def get_autoagent_workspace(autoagentid):
        result=""
        if autoagentid!=0:
            autoagent=DAL_AutoAgent.get_autoagent(autoagentid)
            result=autoagent.AAgentWorkSpace
        return result
    
    @staticmethod
    def init_autoagent_form_control(request):
        result=""
        autoagentid=int(request.POST["autoagentid"])
        control_name=request.POST["controlname"]
        if control_name=="AUTOAGENTNAME":
            result=AutoAgentService.get_autoagent_name(autoagentid)
        
        if control_name=="AUTOAGENTOS":
            result=AutoAgentService.get_autoagent_os(autoagentid)
            print(result)

        if control_name=="AUTOAGENTIP":
            result=AutoAgentService.get_autoagent_ip(autoagentid)
            print(result)
            
        if control_name=="AUTOAGENTBROWSER":
            result=AutoAgentService.get_autoagent_browsers(autoagentid)
            
        if control_name=="AUTOAGENTRESERVED":
            result=AutoAgentService.get_autoagent_reserved(autoagentid)
            
        if control_name=="AUTOAGENTWORKSPACE":
            result=AutoAgentService.get_autoagent_workspace(autoagentid)
            
        return result
    
    @staticmethod
    def check_name_exits(agentname):
        return DAL_AutoAgent.get_autoagent_byname(agentname)
    
    @staticmethod
    def check_ip_exits(agentip):
        return DAL_AutoAgent.get_autoagent_byip(agentip)
            
            
            
        
        
               
