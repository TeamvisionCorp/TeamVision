#coding=utf-8
'''
Created on 2016-10-25

@author: zhangtiande
'''
from rest_framework.pagination import PageNumberPagination
# import django_filters

class ProjectPagination(PageNumberPagination):
    page_size =10
    page_size_query_param = 'page_size'
    max_page_size =10000
        