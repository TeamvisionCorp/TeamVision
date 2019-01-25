#coding=utf-8
'''
Created on 2016-12-5

@author: zhangtiande
'''


from django import forms
from doraemon.ci.models import CIServer
from url_filter.filtersets.django import ModelFilterSet

class DeployServerFilterSet(ModelFilterSet):
    class Meta(object):
        model = CIServer
        fields = ['id']
        