#coding=utf-8
'''
Created on 2016-12-5

@author: zhangtiande
'''


from doraemon.ci.models import CITask
from url_filter.filtersets.django import ModelFilterSet

class CITaskFilterSet(ModelFilterSet):
    class Meta(object):
        model = CITask
        fields = ['id','Project','TaskType','Schedule']


        