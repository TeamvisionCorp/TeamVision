#coding=utf-8
'''
Created on 2015-11-16

@author: zhangtiande
'''

from django.http.request import HttpRequest
from django.http import HttpResponse


def save_to_session(request_func):
    def save_request_session(*args,**kwargs):
        if isinstance(args[0],HttpRequest):
            request=args[0]
            if request.method=="GET":
                for parameter in request.GET:
                    request.session[parameter]=request.GET.get(parameter)
            if request.method=="POST":
                for parameter in request.POST:
                    request.session[parameter]=request.POST.get(parameter)
            print(request.session['TTags'])
        return request_func(*args,**kwargs)
    return save_request_session

def check_value_eixts(model):
    def check_request(request_func):
        def value_check(*args,**kwargs):
            if isinstance(args[0],HttpRequest):
                request=args[0]
                filed_name=request.POST["filed"]
                filed_value=request.POST["value"]
                return HttpResponse(model.objects.check_value_exits(filed_name,filed_value))
            else:
                return request_func(*args,**kwargs)
        return value_check
    return check_request
        
                
                
                




                


    