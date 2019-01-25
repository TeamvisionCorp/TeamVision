#coding=utf-8
'''
Created on 2015-9-24

@author: zhangtiande
'''
from doraemon.pagefactory.worker import Worker
from django.template import RequestContext

class AdminPageWorker(Worker):
    '''
    项目页面生成器
    '''
    def __init__(self,request):
        '''
        Constructor
        '''
        Worker.__init__(self, request)
        
    
    def get_left_nav_bar(self,request,pageModel,template_path,**args):
        page=pageModel(request,**args)
        context_fileds={'page':page}
        return self.get_webpart(context_fileds,template_path)
    
    def get_sub_nav_bar(self,request,pageModel,template_path,**args):
        page=pageModel(request,**args)
        context_fileds={'page':page}
        return self.get_webpart(context_fileds,template_path)
        
        