#coding=utf-8
'''
Created on 2016-12-5

@author: zhangtiande
'''


from teamvision.home.models import Agent
from url_filter.filtersets.django import ModelFilterSet

class AutoFilterSet(ModelFilterSet):
    class Meta(object):
        model = Agent
        fields = ['Status']


        