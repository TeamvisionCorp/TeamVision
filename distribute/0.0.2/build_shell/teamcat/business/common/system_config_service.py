#coding=utf-8
'''
Created on 2015-12-2

@author: zhangtiande
'''

from doraemon.home.models import DicData,DicType
from gatesidelib.common.simplelogger import SimpleLogger

class SystemConfigService(object):
    '''
    classdocs
    '''
    
    @staticmethod
    def get_email_config():
        result = {}
        data_type=DicType.objects.get_by_name("EmailConfig")
        allconfigs = DicData.objects.get_datas_bytype(data_type.id)
        for config in allconfigs:
            result[config.DicDataDesc] = config.DicDataName
        return result
    
    @staticmethod
    def get_platform_configs():
        data_type=DicType.objects.get_by_name("Platform")
        platforms = DicData.objects.get_datas_bytype(data_type.id)
        return platforms
    
    @staticmethod
    def get_platform_name(platform_value):
        result=""
        try:
            data_type=DicType.objects.get_by_name("Platform")
            platform = DicData.objects.get_data_byvalue(platform_value,data_type.id)
            result=platform.DicDataName
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    @staticmethod
    def get_build_status(status_value):
        data_type=DicType.objects.get_by_name("BuildStatus")
        build_status = DicData.objects.get_data_byvalue(status_value,data_type.id)
        return build_status.DicDataName
    
    @staticmethod
    def get_permission_types():
        data_type=DicType.objects.get_by_name("AuthPermissionType")
        permission_types= DicData.objects.get_datas_bytype(data_type.id)
        return permission_types
    
    @staticmethod
    def get_permission_type(type_value):
        data_type=DicType.objects.get_by_name("AuthPermissionType")
        permission_type = DicData.objects.get_data_byvalue(type_value,data_type.id)
        return permission_type.DicDataName
    
    @staticmethod
    def get_device_os():
        data_type=DicType.objects.get_by_name("DeviceOS")
        device_os= DicData.objects.get_datas_bytype(data_type.id).order_by("DicDataValue")
        return device_os
    
    @staticmethod
    def get_device_os_version(type_value):
        if type_value==1 or type_value==None or type_value==0:
            data_type=DicType.objects.get_by_name("AndroidVersion")
        if type_value==2:
            data_type=DicType.objects.get_by_name("IOSVersion")
        if type_value==3:
            data_type=DicType.objects.get_by_name("WPVersion")
        device_os_version= DicData.objects.get_datas_bytype(data_type.id).order_by("DicDataValue")
        return device_os_version
    
    @staticmethod
    def get_screen_szie():
        return SystemConfigService.get_dic_datas("ScreenSize").order_by("DicDataValue")
    
    @staticmethod
    def get_device_type():
        return SystemConfigService.get_dic_datas("DeviceType")
    
    @staticmethod
    def get_dic_datas(data_type_name):
        data_type=DicType.objects.get_by_name(data_type_name)
        dic_datas= DicData.objects.get_datas_bytype(data_type.id)
        return dic_datas
    
    
    @staticmethod
    def test_env():
        return SystemConfigService.get_dic_datas("TestEnv")
    
    
    @staticmethod
    def get_jdk_build_tools():
        return SystemConfigService.get_dic_datas("BuildTools").filter(DicDataDesc='JDK')
    
    @staticmethod
    def get_gradle_build_tools():
        return SystemConfigService.get_dic_datas("BuildTools").filter(DicDataDesc='GRADLE')
    
    @staticmethod
    def get_xcode_build_tools():
        return SystemConfigService.get_dic_datas("BuildTools").filter(DicDataDesc='XCODE')
    
    @staticmethod
    def get_pods_build_tools():
        return SystemConfigService.get_dic_datas("BuildTools").filter(DicDataDesc='PODS')
    
    @staticmethod
    def get_credential_type():
        return SystemConfigService.get_dic_datas("CICredentialType")
    
    @staticmethod
    def get_git_strategy_type():
        return SystemConfigService.get_dic_datas("GitCheckOutStrategy")
    
    @staticmethod
    def get_svn_strategy_type():
        return SystemConfigService.get_dic_datas("SvnCheckOutStrategy")
    
    @staticmethod
    def get_credential(data_value):
        return SystemConfigService.get_dic_data_name("CICredentialType",data_value)
    
    @staticmethod
    def get_file_type_white_list():
        value=SystemConfigService.get_dic_data_name("CIUploadFileLimit",1)
        return eval(value)
    
    @staticmethod
    def get_upload_file_maxsize():
        value=SystemConfigService.get_dic_data_name("CIUploadFileLimit",2)
        return eval(value)   
    
    @staticmethod
    def get_device_version_name(os_type,type_value):
        if os_type==1 or os_type==0:
            type_name="AndroidVersion"
        if os_type==2:
            type_name="IOSVersion"
        if os_type==3:
            type_name="WPVersion"
        return SystemConfigService.get_dic_data_name(type_name, type_value)
    
    @staticmethod
    def get_device_screen_size(data_value):
        return SystemConfigService.get_dic_data_name("ScreenSize",data_value)
    
    @staticmethod
    def get_device_status(data_value):
        return SystemConfigService.get_dic_data_name("DeviceStatus",data_value)
    
    @staticmethod
    def get_noproject_name(data_value):
        return SystemConfigService.get_dic_data_name("NoProject",data_value)
        
    
    
    @staticmethod
    def get_dic_data_name(data_type_name,data_value):
        data_type=DicType.objects.get_by_name(data_type_name)
        dic_data = DicData.objects.get_data_byvalue(data_value,data_type.id)
        return dic_data.DicDataName
    
    
    
    

    
    
    
        