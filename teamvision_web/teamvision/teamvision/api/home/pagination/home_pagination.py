#coding=utf-8
'''
Created on 2018-06-06

@author: zhangtiande
'''
from rest_framework.pagination import PageNumberPagination

class HomeActivityPagination(PageNumberPagination):
    page_size =20
    page_size_query_param = 'page_size'
    max_page_size =10000
