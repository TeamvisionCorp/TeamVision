#coding=utf-8
'''
Created on 2015-9-24

@author: Devuser
'''
from teamvision.pagefactory.worker import Worker
from django.template import RequestContext

class UserCenterPageWorker(Worker):
    '''
    项目页面生成器
    '''
    def __init__(self,request):
        '''
        Constructor
        '''
        Worker.__init__(self, request)
    
    def get_left_nav_bar(self,request,pageModel,userid,template_path,**args):
        context_instance=RequestContext(request)
        page=pageModel(request,userid,**args)
        context_fileds={'page':page,'context_instance':context_instance}
        return self.get_webpart(context_fileds,template_path)
    
    def get_sub_nav_bar(self,request,pageModel,userid,template_path,**args):
        context_instance=RequestContext(request)
        page=pageModel(request,userid,**args)
        context_fileds={'page':page,'context_instance':context_instance}
        return self.get_webpart(context_fileds,template_path)
        
        