#coding=utf-8
# coding=utf8
'''
Created on 2014-1-14
 
@author: zhangtiande
'''
from dataaccess.common.dal_user import DAL_User
from dataaccess.common.dal_dictvalue import DAL_DictValue
from dataaccess.automationtesting.dal_autotestconfig import DAL_AutoTestConfig
from doraemon.automationtesting.models import AutoTestConfig
from gatesidelib.common.simplelogger import SimpleLogger
from dataaccess.automationtesting.dal_automobiledevice import DAL_AutoMobileDevice


import time

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
 
class AutoTestConfigService(object):
    '''
    business for Test submition
    '''
     
    @staticmethod
    def vm_get_all_autotestconfig(request):
        try:
            pageindex = int(request.POST['pageindex'])
            searchkeyword = request.POST['searchkeyword']
            result = AutoTestConfigService.search_autotestconfig(searchkeyword)
        except Exception as ex:
            print(ex)
        return result[15*(pageindex-1):15*pageindex]
    
    @staticmethod
    def get_autotestconfig_page_counts(request):
        try:
            searchkeyword = request.POST['searchkeyword']
            result = AutoTestConfigService.search_autotestconfig(searchkeyword)
        except Exception as ex:
            print(ex)
        return len(result)/15+1
    
    @staticmethod
    def get_autotestconfig_by_group(user,autotestconfiglist):
        resultlist=list()
        if user.has_perm('autotestconfig.view_all_autotestconfig'):
            return autotestconfiglist
        for autotestconfig in autotestconfiglist:
            if str(user.id) in eval(autotestconfig.autotestconfig.TJTester):
                resultlist.append(autotestconfig)
        return resultlist
     
    @staticmethod
    def search_autotestconfig(searchkeyword):
        if searchkeyword == "ALL":
            result = DAL_AutoTestConfig.get_all().filter(TCFIsActive=1)
        else:
            result = AutoTestConfigService.search_autotestconfig_byid(searchkeyword)
            if  result ==None or len(result)==0:
                result = AutoTestConfigService.search_autotestconfig_byname(searchkeyword.strip())
        return result.order_by("-id")
    
    @staticmethod
    def filterautotestconfig(result,requestuser):
        result=AutoTestConfigService.filter_autotestconfig_submtion_type(result, requestuser)
        return result
    
    @staticmethod
    def filter_autotestconfig_by_autotestconfig_status(autotestconfigstatus,result):
        if autotestconfigstatus=="0":
            return result
        return result.filter(TJStatus=autotestconfigstatus)
        
    
    @staticmethod
    def search_autotestconfig_byid(autotestconfigid):
        autotestconfig = None
        try:
            autotestconfig = DAL_AutoTestConfig.get_all().filter(id=autotestconfigid)
        except Exception as ex:
            SimpleLogger.error(ex.message)
        return autotestconfig
     
    @staticmethod
    def search_autotestconfig_byname(autotestconfigname):
        result = None
        try:
            result = DAL_AutoTestConfig.get_all().filter(TaskName__icontains=autotestconfigname)
        except Exception as ex:
            print(ex)
        return result
    
    @staticmethod
    def dm_createautotestconfig(request):
        ''' create new  db model autotestconfig
        '''
        message = "successful"
        try:
            autotestconfig = AutoTestConfig()
            autotestconfig = AutoTestConfigService.initlize_dm_instance(request,autotestconfig)
            DAL_AutoTestConfig.add_autotestconfig(autotestconfig)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.error(message)
            print(message)
        return message
    
    
    @staticmethod
    def disable_autotestconfig(request):
        message = "successful"
        try:
            autotestconfig=DAL_AutoTestConfig.get_autotest_config(request.POST["autotestconfigid"])
            autotestconfig.TaskIsActive=0
            DAL_AutoTestConfig.add_autotestconfig(autotestconfig)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.error(message)
        return message
    
    @staticmethod
    def copy_autotestconfig(request):
        message = "successful"
        try:
            from_autotestconfig=DAL_AutoTestConfig.get_autotest_config(request.POST["autotestconfigid"])
            to_autotestconfig=AutoTestConfig()
            to_autotestconfig.TCFBrowser=from_autotestconfig.TCFBrowser
            to_autotestconfig.TCFCodeURL=from_autotestconfig.TCFCodeURL
            to_autotestconfig.TCFIsActive=from_autotestconfig.TCFIsActive
            to_autotestconfig.TCFIsSplit=from_autotestconfig.TCFIsSplit
            to_autotestconfig.TCFName=from_autotestconfig.TCFName+str(time.time())
            to_autotestconfig.TCFOS=from_autotestconfig.TCFOS
            to_autotestconfig.TCFOSVersion=from_autotestconfig.TCFOSVersion
            to_autotestconfig.TCFProjectID=from_autotestconfig.TCFProjectID
            to_autotestconfig.TCFProjectVersion=from_autotestconfig.TCFProjectVersion
            to_autotestconfig.TCFRunTiming=from_autotestconfig.TCFRunTiming
            to_autotestconfig.TCFTaskTpye=from_autotestconfig.TCFTaskTpye
            to_autotestconfig.TCFTestingEnv=from_autotestconfig.TCFTestingEnv
            to_autotestconfig.TCFViewScope=from_autotestconfig.TCFViewScope
            DAL_AutoTestConfig.add_autotestconfig(to_autotestconfig)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.error(message)
        return message
            
        
         
                   
    @staticmethod
    def dm_updateautotestconfig(request):
        message = "successful"
        try:
            autotestconfig=DAL_AutoTestConfig.get_autotest_config(request.POST["autotestconfigid"])
            autotestconfig = AutoTestConfigService.initlize_dm_instance(request,autotestconfig)
            DAL_AutoTestConfig.add_autotestconfig(autotestconfig)
        except Exception as ex:
            message = str(ex)
            print(ex)
            SimpleLogger.error(message)
        return message
    
           
    @staticmethod
    def check_name_exits(request):
        return DAL_AutoTestConfig.check_name_exits(request.POST['autotestconfigname'])

    
      
    @staticmethod
    def initlize_dm_instance(request, autotestconfig):
        autotestconfig.TCFName=request.POST.get("TCFName")
        autotestconfig.TCFProjectID=int(request.POST.get("TCFProject"))
        autotestconfig.TCFProjectVersion=request.POST.get("TCFProjectVersion")
        autotestconfig.TCFTaskTpye =int(request.POST.get("TCFTaskTpye"))
        print("step1")
        if autotestconfig.TCFTaskTpye==3:
            print("step2")
            autotestconfig.TCFOS= request.POST.get("TCFOS")
            print(autotestconfig.TCFOS)
            autotestconfig.TCFOSVersion=request.POST.get("TCFOSVersion")
        
        if autotestconfig.TCFTaskTpye==2:
            autotestconfig.TCFTestingEnv=int(request.POST.get("TCFTestingEnv"))
            autotestconfig.TCFBrowser=request.POST.get("TCFBrowser")
        
        autotestconfig.TCFRunTiming=str(request.POST.get("TCFRunTiming"))
        autotestconfig.TCFIsSplit=int(request.POST.get("TCFIsSplit"))
        autotestconfig.TCFViewScope=int(request.POST.get("TCFViewScope"))
        autotestconfig.TCFCodeURL=request.POST.get("TCFCodeURL")
        autotestconfig.TCFExecuteDriver=request.POST.get("TCFExecuteDriver")
        autotestconfig.TCFDriverArgs=request.POST.get("TCFDriverArgs")
        
        return autotestconfig
             
     

     
    @staticmethod
    def get_autotestconfig_types(autotestconfigid):
        tasktypes = DAL_DictValue.getdatavaluebytype("AutoTaskType")
        result=list()
        for tasktype in tasktypes:
            temp=dict()
            temp["text"]=tasktype.DicDataName
            temp["memberid"]=tasktype.DicDataValue
            if autotestconfigid!=0:
                autotestconfig=DAL_AutoTestConfig.get_autotest_config(autotestconfigid)
                if tasktype.DicDataValue==autotestconfig.TCFTaskTpye:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
     
        

    @staticmethod
    def getdicvaluebyid(id):
        dicdata = DAL_DictValue.getdatavaluebyid(id)
        if dicdata:
            return dicdata.DicDataName
        else:
            return "--"
                 
     
     
  
        
    
    @staticmethod
    def get_autotestconfig_name(autotestconfigid):
        result=""
        if autotestconfigid!=0:
            autotestconfig=DAL_AutoTestConfig.get_autotest_config(autotestconfigid)
            result=autotestconfig.TCFName
        return result
    
    @staticmethod
    def get_autotestconfig_codeurl(autotestconfigid):
        result=""
        if autotestconfigid!=0:
            autotestconfig=DAL_AutoTestConfig.get_autotest_config(autotestconfigid)
            result=autotestconfig.TCFCodeURL
        return result
    
    @staticmethod
    def get_autotestconfig_testconfig(autotestconfigid):
        pass
#         all_testingconfigs=DAL_TestingConfig.get_all()
#         result=list()
#         for testingconfig in all_testingconfigs:
#             temp=dict()
#             temp["text"]=testingconfig.TCFName
#             temp["memberid"]=testingconfig.id
#             if autotestconfigid!=0:
#                 autotestconfig=DAL_AutoTestConfig.get_autotest_config(autotestconfigid)
#                 if testingconfig.id==autotestconfig.TestingConfigID:
#                     temp["selected"]=1
#                 else:
#                     temp["selected"]=0
#             else:
#                 temp["selected"]=0
#             result.append(temp)
#         return str(result).replace("u'","'")
    
    
    @staticmethod
    def get_autotestconfig_runtiming(autotestconfigid):
        result=""
        if autotestconfigid!=0:
            autotestconfig=DAL_AutoTestConfig.get_autotest_config(autotestconfigid)
            result=autotestconfig.TCFRunTiming
        return result
    
    
    @staticmethod
    def get_autotestconfig_projests(autotestconfigid):
        pass
        all_projects=list()
        result=list()
        for project in all_projects:
            temp=dict()
            temp["text"]=project.TPName
            temp["memberid"]=project.id
            if autotestconfigid!=0:
                autotestconfig=DAL_AutoTestConfig.get_autotest_config(autotestconfigid)
                if project.id==autotestconfig.TCFProjectID:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    @staticmethod
    def get_autotestconfig_issplit(autotestconfigid):
        result=1
        if autotestconfigid!=0:
            autotestconfig=DAL_AutoTestConfig.get_autotest_config(autotestconfigid)
            result=autotestconfig.TCFIsSplit
        return result
    
    @staticmethod
    def get_autotestconfig__viewscope(autotestconfigid):
        result=1
        if autotestconfigid!=0:
            autotestconfig=DAL_AutoTestConfig.get_autotest_config(autotestconfigid)
            result=autotestconfig.TCFViewScope
        return result
    
    @staticmethod
    def get_autotestconfig_driver(autotestconfigid):
        alldrivers=DAL_DictValue.getdatavaluebytype("AutoAgentExecDriver")
        result=list()
        for driver in alldrivers:
            temp=dict()
            temp["text"]=driver.DicDataName
            temp["memberid"]=driver.id
            if autotestconfigid!=0:
                autotestconfig=DAL_AutoTestConfig.get_autotest_config(autotestconfigid)
                if driver.DicDataValue==autotestconfig.TCFExecuteDriver:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")

    @staticmethod
    def get_autotestconfig_projectversion(autotestconfigid,projectid):
        projectversions=list()
        result=list()
        for version in projectversions:
            temp=dict()
            temp["text"]=version.PVVersion
            temp["memberid"]=version.id
            if autotestconfigid!=0:
                autotestconfig=DAL_AutoTestConfig.get_autotest_config(autotestconfigid)
                if version.id==int(autotestconfig.TCFProjectVersion):
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    
    @staticmethod
    def get_autotestconfig_testingenv(autotestconfigid):
        all_testenvs=DAL_DictValue.getdatavaluebytype("TestEnv")
        result=list()
        for env in all_testenvs:
            temp=dict()
            temp["text"]=env.DicDataName
            temp["memberid"]=env.id
            if autotestconfigid!=0:
                autotestconfig=DAL_AutoTestConfig.get_autotest_config(autotestconfigid)
                
                if autotestconfig.TCFTestingEnv and  env.DicDataValue==int(autotestconfig.TCFTestingEnv):
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    @staticmethod
    def get_autotestconfig_os(autotestconfigid):
        all_os=DAL_DictValue.getdatavaluebytype("AutoTaskRuntime").filter(DicDataDesc='APP')
        result=list()
        if autotestconfigid!=0:
            autotestconfig=DAL_AutoTestConfig.get_autotest_config(autotestconfigid)
        for os in all_os:
            temp=dict()
            temp["text"]=os.DicDataName
            temp["memberid"]=os.DicDataValue
            print(temp)
            if autotestconfigid!=0:
                if os.DicDataValue==autotestconfig.TCFOS:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    
    
    @staticmethod
    def get_autotestconfig_browsers(autotestconfigid):
        all_browsers=DAL_DictValue.getdatavaluebytype("AutoTaskRuntime").filter(DicDataDesc='WEB')
        result=list()
        if autotestconfigid!=0:
            autotestconfig=DAL_AutoTestConfig.get_autotest_config(autotestconfigid)
        for browser in all_browsers:
            temp=dict()
            temp["text"]=browser.DicDataName
            temp["memberid"]=browser.DicDataValue
            if autotestconfigid!=0 and autotestconfig.TCFBrowser:
                if browser.DicDataValue in eval(autotestconfig.TCFBrowser):
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    @staticmethod
    def get_autotestconfig_osversion(autotestconfigid,osid):
        osname=DAL_DictValue.get_dataname_by_datavalue("AutoTaskRuntime",osid).DicDataName
        if osname=="Android":
            mobiledevice=DAL_AutoMobileDevice.get_device_byos("android")
        else:
            mobiledevice=DAL_AutoMobileDevice.get_device_byos("ios")
        result=list()
        for device in mobiledevice:
            temp=dict()
            temp["text"]=device.MDOSVersion
            temp["value"]=device.MDOSVersion
            if autotestconfigid!=0:
                autotestconfig=DAL_AutoTestConfig.get_autotest_config(autotestconfigid)
                if device.MDOSVersion==autotestconfig.TCFOSVersion:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    @staticmethod
    def get_autotestconfig_driver_args(autotestconfigid):
        result=""
        if autotestconfigid!=0:
            autotestconfig=DAL_AutoTestConfig.get_autotest_config(autotestconfigid)
            result=autotestconfig.TCFDriverArgs
        return result

    
    @staticmethod
    def init_autotestconfig_form_control(request):
        result=""
        autotestconfigid=int(request.POST["autotestconfigid"])
        control_name=request.POST["controlname"]
        if control_name=="AUTOTESTCONFIGTASKTYPE":
            result=AutoTestConfigService.get_autotestconfig_types(autotestconfigid)
            
        if control_name=="AUTOTESTCONFIGNAME":
            result=AutoTestConfigService.get_autotestconfig_name(autotestconfigid)
            
        if control_name=="AUTOTESTCONFIGCODEURL":
            result=AutoTestConfigService.get_autotestconfig_codeurl(autotestconfigid)
            
        if control_name=="AUTOTESTCONFIGVERSION":
            projectid=int(request.POST['projectid'])
            result=AutoTestConfigService.get_autotestconfig_projectversion(autotestconfigid,projectid)
            
        if control_name=="AUTOTESTCONFIGRUNTIMING":
            result=AutoTestConfigService.get_autotestconfig_runtiming(autotestconfigid)
            
        if control_name=="AUTOTESTCONFIGPROJECT":
            result=AutoTestConfigService.get_autotestconfig_projests(autotestconfigid)
            
        if control_name=="AUTOTESTCONFIGSPLIT":
            result=AutoTestConfigService.get_autotestconfig_issplit(autotestconfigid)
            
        if control_name=="AUTOTESTCONFIGVIEWSCOPE":
            result=AutoTestConfigService.get_autotestconfig__viewscope(autotestconfigid)
            
        if control_name=="AUTOTESTCONFIGDRIVER":
            result=AutoTestConfigService.get_autotestconfig_driver(autotestconfigid)
        
        if control_name=="AUTOTESTCONFIGDRIVERARGS":
            result=AutoTestConfigService.get_autotestconfig_driver_args(autotestconfigid)
            
        if control_name=="AUTOTESTCONFIGTESTINGENV":
            result=AutoTestConfigService.get_autotestconfig_testingenv(autotestconfigid)
            
        if control_name=="AUTOTESTCONFIGBROWSER":
            result=AutoTestConfigService.get_autotestconfig_browsers(autotestconfigid)
        
        if control_name=="AUTOTESTCONFIGOS":
            result=AutoTestConfigService.get_autotestconfig_os(autotestconfigid)
        
        if control_name=="AUTOTESTCONFIGOSVERSION":
            osid=int(request.POST['os'])
            result=AutoTestConfigService.get_autotestconfig_osversion(autotestconfigid,osid)
            print(result)
            
        return result
            
            
            
        
        
               
