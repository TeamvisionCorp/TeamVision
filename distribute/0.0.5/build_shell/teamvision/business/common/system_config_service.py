#coding=utf-8
'''
Created on 2015-12-2

@author: zhangtiande
'''

from teamvision.home.models import DicData,DicType
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
            result[config.DicDataName] = config.DicDataValue
        return result

    
    @staticmethod
    def get_dic_datas(data_type_name):
        data_type=DicType.objects.get_by_name(data_type_name)
        dic_datas= DicData.objects.get_datas_bytype(data_type.id)
        return dic_datas

    @staticmethod
    def save_dic_datas(dic_datas):
        result = list()
        for dicdata_list in dic_datas:
            for dic_data in dicdata_list.get("DicDatas"):
                temp_data = SystemConfigService.init_dicdata(dic_data)
                result.append(temp_data)
        return result

    @staticmethod
    def init_dicdata(dicdata_json):
        if dicdata_json is not None:
            id = dicdata_json.get("id",0)
            dicdata = DicData.objects.get(int(id))
            if dicdata is not None:
                dicdata.DicDataValue = dicdata_json.get("DicDataValue","")
                dicdata.save()
            return dicdata





    
    @staticmethod
    def get_git_strategy_type():
        return SystemConfigService.get_dic_datas("GitCheckOutStrategy")

    @staticmethod
    def get_svn_strategy_type():
        return SystemConfigService.get_dic_datas("SvnCheckOutStrategy")

    
    @staticmethod
    def get_file_type_white_list():
        value=SystemConfigService.get_dic_data_name("UploadFileLimit","white_list")
        return eval(value)
    
    @staticmethod
    def get_upload_file_maxsize():
        value=SystemConfigService.get_dic_data_name("UploadFileLimit","max_size")
        return eval(value)
    
    @staticmethod
    def get_noproject_name(data_value):
        return SystemConfigService.get_dic_data_name("NoProject",data_value)
        
    
    
    @staticmethod
    def get_dic_data_name(data_type_name,data_name):
        data_type=DicType.objects.get_by_name(data_type_name)
        dic_data = DicData.objects.get_data_byname(data_name,data_type.id)
        return dic_data.DicDataValue
    
    
    
    

    
    
    
        