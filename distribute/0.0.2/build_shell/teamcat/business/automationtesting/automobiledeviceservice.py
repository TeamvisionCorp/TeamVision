#coding=utf-8
# coding=utf8
'''
Created on 2014-1-14
 
@author: zhangtiande
'''
from doraemon.automationtesting.models import AutoMobileDevice
from dataaccess.automationtesting.dal_automobiledevice import DAL_AutoMobileDevice
from dataaccess.common.dal_user import DAL_User
from dataaccess.common.dal_dictvalue import DAL_DictValue
from gatesidelib.common.simplelogger import SimpleLogger


import time

# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
 
class AutoMobileDeviceService(object):
    '''
    business for Test submition
    '''
     
    @staticmethod
    def vm_getall_automobiledevice(request):
        try:
            pageindex = int(request.POST['pageindex'])
            searchkeyword = request.POST['searchkeyword']
            result = AutoMobileDeviceService.search_automobiledevice(searchkeyword)
        except Exception as ex:
            print(ex)
        return result[15*(pageindex-1):15*pageindex]

    @staticmethod
    def get_automobiledevice_page_counts(request):
        try:
            searchkeyword = request.POST['searchkeyword']
            result = AutoMobileDeviceService.search_automobiledevice(searchkeyword)
        except Exception as ex:
            print(ex)
        return len(result)/15+1
    
    @staticmethod
    def get_automobiledevice_by_group(user,automobiledevicelist):
        resultlist=list()
        if user.has_perm('automobiledevice.view_all_automobiledevice'):
            return automobiledevicelist
        for automobiledevice in automobiledevicelist:
            if str(user.id) in eval(automobiledevice.automobiledevice.TJTester):
                resultlist.append(automobiledevice)
        return resultlist
     
    @staticmethod
    def search_automobiledevice(searchkeyword):
        if searchkeyword == "ALL":
            result = DAL_AutoMobileDevice.get_all().filter(MDIsActive=1)
        else:
            result = AutoMobileDeviceService.search_automobiledevice_byid(searchkeyword)
            if  result ==None or len(result)==0:
                result = AutoMobileDeviceService.search_automobiledevice_byname(searchkeyword.strip())
        return result.order_by("-id")
    
    @staticmethod
    def filterautomobiledevice(result,requestuser):
        result=AutoMobileDeviceService.filter_automobiledevice_submtion_type(result, requestuser)
        return result
    
    @staticmethod
    def filter_automobiledevice_by_automobiledevice_status(automobiledevicestatus,result):
        if automobiledevicestatus=="0":
            return result
        return result.filter(TJStatus=automobiledevicestatus)
        
    
        
     
    @staticmethod
    def search_automobiledevice_byid(automobiledeviceid):
        automobiledevice = None
        try:
            automobiledevice = DAL_AutoMobileDevice.get_all().filter(id=automobiledeviceid)
        except Exception as ex:
            SimpleLogger.error(ex.message)
        return automobiledevice
     
    @staticmethod
    def search_automobiledevice_byname(automobiledevicename):
        result = None
        try:
            result = DAL_AutoMobileDevice.get_all().filter(AName__icontains=automobiledevicename)
        except Exception as ex:
            print(ex)
        return result
    
    @staticmethod
    def dm_createautomobiledevice(request):
        ''' create new  db model automobiledevice
        '''
        message = "successful"
        try:
            automobiledevice = AutoMobileDevice()
            automobiledevice = AutoMobileDeviceService.initlize_dm_instance(request,automobiledevice)
            DAL_AutoMobileDevice.add_automobiledevice(automobiledevice)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.error(message)
        return message
    
    
    @staticmethod
    def disable_automobiledevice(request):
        
        message = "successful"
        try:
            automobiledevice=DAL_AutoMobileDevice.get_automobiledevice(request.POST["automobiledeviceid"])
            automobiledevice.TaskIsActive=0
            DAL_AutoMobileDevice.add_automobiledevice(automobiledevice)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.error(message)
        return message
    
    @staticmethod
    def copy_automobiledevice(request):
        message = "successful"
        try:
            from_automobiledevice=DAL_AutoMobileDevice.get_automobiledevice(request.POST["automobiledeviceid"])
            to_automobiledevice=AutoMobileDevice()
            to_automobiledevice.AName=from_automobiledevice.AName
            to_automobiledevice.AOS=from_automobiledevice.AOS
            to_automobiledevice.AIP=from_automobiledevice.AIP
            to_automobiledevice.AStatus=1
            to_automobiledevice.AAgentBrowser=from_automobiledevice.AAgentBrowser
            to_automobiledevice.AIsReserved=from_automobiledevice.AIsReserved
            DAL_AutoMobileDevice.add_automobiledevice(to_automobiledevice)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.error(message)
        return message
            
        
         
                   
    @staticmethod
    def dm_updateautomobiledevice(request):
        message = "successful"
        try:
            automobiledevice=DAL_AutoMobileDevice.get_automobiledevice(request.POST["automobiledeviceid"])
            automobiledevice = AutoMobileDeviceService.initlize_dm_instance(request,automobiledevice)
            DAL_AutoMobileDevice.add_automobiledevice(automobiledevice)
        except Exception as ex:
            message = str(ex)
            SimpleLogger.error(message)
        return message
    
           
            
      
    @staticmethod
    def initlize_dm_instance(request, automobiledevice):
        
        automobiledevice.AName=request.POST.get("AName")
        automobiledevice.AOS=int(request.POST.get("AOS"))
        automobiledevice.AIP=request.POST.get("AIP")
        automobiledevice.AAgentBrowser = request.POST.get("AAgentBrowser")
        if ',' not in automobiledevice.AAgentBrowser:
            automobiledevice.AAgentBrowser=automobiledevice.AAgentBrowser+","
        automobiledevice.AStatus=1
        automobiledevice.AIsReserved=int(request.POST.get("AIsReserved"))
        return automobiledevice
             
     
    @staticmethod
    def get_automobiledevice_namelist():
        automobiledevicelist = DAL_AutoMobileDevice.get_all()
        return str([item.TaskName for item in automobiledevicelist]).replace("u'","'")

     
    @staticmethod
    def get_automobiledevice_types(automobiledeviceid):
        tasktypes = DAL_DictValue.getdatavaluebytype("AutoTaskType")
        result=list()
        for tasktype in tasktypes:
            temp=dict()
            temp["text"]=tasktype.DicDataName
            temp["memberid"]=tasktype.DicDataValue
            if automobiledeviceid!=0:
                automobiledevice=DAL_AutoMobileDevice.get_automobiledevice(automobiledeviceid)
                if tasktype.DicDataValue==automobiledevice.TaskTpye:
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
    def get_automobiledevice_name(automobiledeviceid):
        result=""
        if automobiledeviceid!=0:
            automobiledevice=DAL_AutoMobileDevice.get_automobiledevice(automobiledeviceid)
            result=automobiledevice.AName
        return result
    
    @staticmethod
    def get_automobiledevice_os(automobiledeviceid):
        all_os=DAL_DictValue.getdatavaluebytype("AgentOSType")
        result=list()
        if automobiledeviceid!=0:
            automobiledevice=DAL_AutoMobileDevice.get_automobiledevice(automobiledeviceid)
        for os in all_os:
            temp=dict()
            temp["text"]=os.DicDataName
            temp["memberid"]=os.DicDataValue
            if automobiledeviceid!=0:
                if os.DicDataValue==automobiledevice.AOS:
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    
    
    @staticmethod
    def get_automobiledevice_browsers(automobiledeviceid):
        all_browsers=DAL_DictValue.getdatavaluebytype("AutoTaskRuntime").filter(DicDataDesc='WEB')
        result=list()
        if automobiledeviceid!=0:
            automobiledevice=DAL_AutoMobileDevice.get_automobiledevice(automobiledeviceid)
        for browser in all_browsers:
            temp=dict()
            temp["text"]=browser.DicDataName
            temp["memberid"]=browser.DicDataValue
            if automobiledeviceid!=0:
                if browser.DicDataValue in eval(automobiledevice.AAgentBrowser):
                    temp["selected"]=1
                else:
                    temp["selected"]=0
            else:
                temp["selected"]=0
            result.append(temp)
        return str(result).replace("u'","'")
    
    @staticmethod
    def get_automobiledevice_ip(automobiledeviceid):
        result=""
        if automobiledeviceid!=0:
            automobiledevice=DAL_AutoMobileDevice.get_automobiledevice(automobiledeviceid)
            result=automobiledevice.AIP
        return result
    
    @staticmethod
    def get_automobiledevice_reserved(automobiledeviceid):
        result=1
        if automobiledeviceid!=0:
            automobiledevice=DAL_AutoMobileDevice.get_automobiledevice(automobiledeviceid)
            result=automobiledevice.AIsReserved
        return result
    
    @staticmethod
    def init_automobiledevice_form_control(request):
        result=""
        automobiledeviceid=int(request.POST["automobiledeviceid"])
        control_name=request.POST["controlname"]
        if control_name=="AUTOAGENTNAME":
            result=AutoMobileDeviceService.get_automobiledevice_name(automobiledeviceid)
        
        if control_name=="AUTOAGENTOS":
            result=AutoMobileDeviceService.get_automobiledevice_os(automobiledeviceid)

        if control_name=="AUTOAGENTIP":
            result=AutoMobileDeviceService.get_automobiledevice_ip(automobiledeviceid)
            print(result)
            
        if control_name=="AUTOAGENTBROWSER":
            result=AutoMobileDeviceService.get_automobiledevice_browsers(automobiledeviceid)
            
        if control_name=="AUTOAGENTRESERVED":
            result=AutoMobileDeviceService.get_automobiledevice_reserved(automobiledeviceid)
        return result
            
            
            
        
        
               
