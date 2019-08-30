#coding=utf-8
'''
Created on 2016-12-5

@author: zhangtiande
'''


from teamvision.home.models import DicType
from url_filter.filtersets.django import ModelFilterSet

class DicTypeFilterSet(ModelFilterSet):
    class Meta(object):
        model = DicType
        fields = ['id','Scope']