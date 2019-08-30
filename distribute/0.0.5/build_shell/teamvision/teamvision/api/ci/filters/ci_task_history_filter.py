#coding=utf-8
'''
Created on 2016-12-5

@author: zhangtiande
'''


from teamvision.ci.models import CITaskHistory,CITaskStepOutput,CITaskStageHistory
from url_filter.filtersets.django import ModelFilterSet


class CITaskHistoryFilterSet(ModelFilterSet):
    class Meta(object):
        model = CITaskHistory
        fields = ['id','CITaskID','TaskUUID','Status']


class CITaskStageHistoryFilterSet(ModelFilterSet):
    class Meta(object):
        model = CITaskStageHistory
        fields = ['id','TaskID','TQUUID','TaskHistoryID','StageID']


class CITaskStepOutPutFilterSet(ModelFilterSet):
    class Meta(object):
        model = CITaskStepOutput
        fields = ['id','TaskID','StageHistoryID','TaskHistoryID']