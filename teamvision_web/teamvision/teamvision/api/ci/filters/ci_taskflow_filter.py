# coding=utf-8
'''
Created on 2016-12-5

@author: zhangtiande
'''

from teamvision.ci.models import CITaskFlow, CIFlowSectionHistory, CITaskFlowHistory
from url_filter.filtersets.django import ModelFilterSet


class CITaskFlowFilterSet(ModelFilterSet):
    class Meta(object):
        model = CITaskFlow
        fields = ['id', 'Project']


class CITaskFlowHistoryFilterSet(ModelFilterSet):
    class Meta(object):
        model = CITaskFlowHistory
        fields = ['id', 'TQUUID', 'Status', 'TaskFlow']


class CIFlowSectionHistoryFilterSet(ModelFilterSet):
    class Meta(object):
        model = CIFlowSectionHistory
        fields = ['id', 'TQUUID', 'Status', 'TaskFlow', 'TaskFlowHistory', 'Section']
