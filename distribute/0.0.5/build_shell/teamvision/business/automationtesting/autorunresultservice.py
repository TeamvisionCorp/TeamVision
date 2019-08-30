#coding=utf-8
# coding=utf8
'''
Created on 2014-1-14
 
@author: zhangtiande
'''
from teamvision.automationtesting.models import AutoRunResult
from dataaccess.automationtesting.dal_autorunresult import DAL_AutoRunResult
from dataaccess.common.dal_user import DAL_User
from dataaccess.common.dal_dictvalue import DAL_DictValue
from gatesidelib.common.simplelogger import SimpleLogger


import time

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
 
class AutoRunResultService(object):
    '''
    business for Test submition
    '''
     
    @staticmethod
    def vm_getall_autorunresult(request):
        try:
            pageindex = int(request.POST['pageindex'])
            searchkeyword = request.POST['searchkeyword']
            result = AutoRunResultService.search_autorunresult(searchkeyword)
        except Exception as ex:
            print(ex)
        return result[15*(pageindex-1):15*pageindex]
    
    @staticmethod
    def get_autorunresult_page_counts(request):
        try:
            searchkeyword = request.POST['searchkeyword']
            result = AutoRunResultService.search_autorunresult(searchkeyword)
        except Exception as ex:
            print(ex)
        return len(result)/15+1
    
     
    @staticmethod
    def search_autorunresult(searchkeyword):
        if searchkeyword == "ALL":
            result = DAL_AutoRunResult.get_all()
        else:
            result = AutoRunResultService.search_autorunresult_byid(searchkeyword)
            if  result ==None or len(result)==0:
                result = AutoRunResultService.search_autorunresult_byname(searchkeyword.strip())
        return result.order_by("-id")
    
    @staticmethod
    def filterautorunresult(result,requestuser):
        result=AutoRunResultService.filter_autorunresult_submtion_type(result, requestuser)
        return result

        
    
        
     
    @staticmethod
    def search_autorunresult_byid(autorunresultid):
        autorunresult = None
        try:
            autorunresult = DAL_AutoRunResult.get_all().filter(id=autorunresultid)
        except Exception as ex:
            SimpleLogger.error(ex.message)
        return autorunresult
     
    @staticmethod
    def search_autorunresult_byname(autorunresultname):
        result = None
        try:
            result = DAL_AutoRunResult.get_all().filter(AName__icontains=autorunresultname)
        except Exception as ex:
            print(ex)
        return result
    
    @staticmethod
    def dm_createautorunresult(request):
        ''' create new  db model autorunresult
        '''
        message = "successful"
        try:
            autorunresult = AutoRunResult()
            autorunresult = AutoRunResultService.initlize_dm_instance(request,autorunresult)
            DAL_AutoRunResult.add_autorunresult(autorunresult)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.error(message)
        return message
    
    
    @staticmethod
    def disable_autorunresult(request):
        
        message = "successful"
        try:
            autorunresult=DAL_AutoRunResult.get_autorunresult(request.POST["autorunresultid"])
            autorunresult.TaskIsActive=0
            DAL_AutoRunResult.add_autorunresult(autorunresult)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.error(message)
        return message
    
    @staticmethod
    def copy_autorunresult(request):
        message = "successful"
        try:
            from_autorunresult=DAL_AutoRunResult.get_autorunresult(request.POST["autorunresultid"])
            to_autorunresult=AutoRunResult()
            to_autorunresult.AName=from_autorunresult.AName
            to_autorunresult.AOS=from_autorunresult.AOS
            to_autorunresult.AIP=from_autorunresult.AIP
            to_autorunresult.AStatus=1
            to_autorunresult.AAgentBrowser=from_autorunresult.AAgentBrowser
            to_autorunresult.AIsReserved=from_autorunresult.AIsReserved
            DAL_AutoRunResult.add_autorunresult(to_autorunresult)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.error(message)
        return message
            
        
         
                   
    @staticmethod
    def dm_updateautorunresult(request):
        message = "successful"
        try:
            autorunresult=DAL_AutoRunResult.get_autorunresult(request.POST["autorunresultid"])
            autorunresult = AutoRunResultService.initlize_dm_instance(request,autorunresult)
            DAL_AutoRunResult.add_autorunresult(autorunresult)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.error(message)
        return message
    
           
            
      
    @staticmethod
    def initlize_dm_instance(request, autorunresult):
        
        autorunresult.AName=request.POST.get("AName")
        autorunresult.AOS=int(request.POST.get("AOS"))
        autorunresult.AIP=request.POST.get("AIP")
        autorunresult.AAgentBrowser = request.POST.get("AAgentBrowser")
        if ',' not in autorunresult.AAgentBrowser:
            autorunresult.AAgentBrowser=autorunresult.AAgentBrowser+","
        autorunresult.AStatus=1
        autorunresult.AIsReserved=int(request.POST.get("AIsReserved"))
        return autorunresult
             
     
    @staticmethod
    def get_autorunresult_namelist():
        autorunresultlist = DAL_AutoRunResult.get_all()
        return str([item.TaskName for item in autorunresultlist]).replace("u'","'")

     
    @staticmethod
    def get_autorunresult_types(autorunresultid):
        tasktypes = DAL_DictValue.getdatavaluebytype("AutoTaskType")
        result=list()
        for tasktype in tasktypes:
            temp=dict()
            temp["text"]=tasktype.DicDataName
            temp["memberid"]=tasktype.DicDataValue
            if autorunresultid!=0:
                autorunresult=DAL_AutoRunResult.get_autorunresult(autorunresultid)
                if tasktype.DicDataValue==autorunresult.TaskTpye:
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
    def get_autorunresult_name(autorunresultid):
        result=""
        if autorunresultid!=0:
            autorunresult=DAL_AutoRunResult.get_autorunresult(autorunresultid)
            result=autorunresult.AName
        return result
    
    @staticmethod
    def get_autorunresult_os(autorunresultid):
        all_os=DAL_DictValue.getdatavaluebytype("AgentOSType")
        result=list()
        if autorunresultid!=0:
            autorunresult=DAL_AutoRunResult.get_autorunresult(autorunresultid)
        for os in all_os:
            temp=dict()
            temp["text"]=os.DicDataName
            temp["memberid"]=os.DicDataValue
            if autorunresultid!=0:
                if os.DicDataValue==autorunresult.AOS:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    
    
    @staticmethod
    def get_autorunresult_browsers(autorunresultid):
        all_browsers=DAL_DictValue.getdatavaluebytype("AutoTaskRuntime").filter(DicDataDesc='WEB')
        result=list()
        if autorunresultid!=0:
            autorunresult=DAL_AutoRunResult.get_autorunresult(autorunresultid)
        for browser in all_browsers:
            temp=dict()
            temp["text"]=browser.DicDataName
            temp["memberid"]=browser.DicDataValue
            if autorunresultid!=0:
                if browser.DicDataValue in eval(autorunresult.AAgentBrowser):
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    @staticmethod
    def get_autorunresult_ip(autorunresultid):
        result=""
        if autorunresultid!=0:
            autorunresult=DAL_AutoRunResult.get_autorunresult(autorunresultid)
            result=autorunresult.AIP
        return result
    
    @staticmethod
    def get_autorunresult_reserved(autorunresultid):
        result=1
        if autorunresultid!=0:
            autorunresult=DAL_AutoRunResult.get_autorunresult(autorunresultid)
            result=autorunresult.AIsReserved
        return result
    
    @staticmethod
    def init_autorunresult_form_control(request):
        result=""
        autorunresultid=int(request.POST["autorunresultid"])
        control_name=request.POST["controlname"]
        if control_name=="AUTOAGENTNAME":
            result=AutoRunResultService.get_autorunresult_name(autorunresultid)
        
        if control_name=="AUTOAGENTOS":
            result=AutoRunResultService.get_autorunresult_os(autorunresultid)

        if control_name=="AUTOAGENTIP":
            result=AutoRunResultService.get_autorunresult_ip(autorunresultid)
            print(result)
            
        if control_name=="AUTOAGENTBROWSER":
            result=AutoRunResultService.get_autorunresult_browsers(autorunresultid)
            
        if control_name=="AUTOAGENTRESERVED":
            result=AutoRunResultService.get_autorunresult_reserved(autorunresultid)
        return result
            
            
            
        
        
               
