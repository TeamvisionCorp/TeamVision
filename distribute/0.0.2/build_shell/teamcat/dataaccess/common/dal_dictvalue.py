#coding=utf-8
# coding=utf-8
'''
Created on 2014-2-17

@author: ETHAN
'''
from doraemon.home.models import DicType,DicData

class DAL_DictValue(object):
    '''
    data access for dictionary table
    '''


    @staticmethod
    def getdatavaluebytype(datatypename):
        dicType=DicType.objects.all().filter(DicTypeName=datatypename).first()
        if dicType:
            return DicData.objects.all().filter(DicType_id=dicType.id)
        else:
            return None
    
    @staticmethod
    def getdatavaluebyid(dataid):
        dicdata=DicData.objects.get(id=dataid)
        return dicdata
    
    
    @staticmethod
    def getdatavaluebydataname(datatypename,dataname):
        dicType=DicType.objects.all().filter(DicTypeName=datatypename).first()
        if dicType:
            dicDataList=DicData.objects.all().filter(DicType_id=dicType.id)
            for dicdata in dicDataList:
                if dicdata.DicDataName==dataname:
                    result=dicdata
        return result
    
    @staticmethod
    def get_dataname_by_datavalue(datatypename,datavalue):
        dicType=DicType.objects.all().filter(DicTypeName=datatypename).first()
        if dicType:
            dicDataList=DicData.objects.all().filter(DicType_id=dicType.id)
            for dicdata in dicDataList:
                if dicdata.DicDataValue==datavalue:
                    result=dicdata
        return result
            
        