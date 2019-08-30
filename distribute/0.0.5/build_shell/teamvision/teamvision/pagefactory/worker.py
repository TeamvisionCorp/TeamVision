#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''

from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext,Context 
from django.template.loader import render_to_string

class Worker(object):
    '''
    项目页面生成器
    '''


    def __init__(self,request):
        '''
        Constructor
        '''
        self.request=request
    
    def get_page(self,pagefileds,template_path,request):
        '''
           pagefileds:key,value paires
        '''
        return render(request,template_path,pagefileds)
    
    
    def get_page_none_args(self,template_path,request):
        return render(request,template_path)
    

    def get_webpart(self,pagefileds,template_path):
        '''
           pagefileds:key,value paires
        '''
        return render_to_string(template_path,pagefileds,self.request)
    
    def get_webpart_none_args(self,template_path):
        return render_to_string(template_path)
        