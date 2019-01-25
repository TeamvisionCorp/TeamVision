#coding=utf-8
'''
Created on 2016-12-5

@author: zhangtiande
'''


from teamvision.ci.models import ServiceHost
from url_filter.filtersets.django import ModelFilterSet

class ServiceHostFilterSet(ModelFilterSet):
    class Meta(object):
        model = ServiceHost
        fields = ['EnvID']
        