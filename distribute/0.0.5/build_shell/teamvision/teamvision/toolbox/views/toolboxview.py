#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext

def index_list(request):
    ''' index page'''
    return render_to_response('tool/toolboxindexview.html',context_instance=RequestContext(request))

def get_toolpage(request):
    "get tool page"
    pagetemplate="<iframe src=\"{PAGEURL}\"  width=\"100%\" height=\"100%\" > </iframe>"
    toolname=request.POST["toolname"]
    if toolname=='nga':
        pagehtml=pagetemplate.replace("{PAGEURL}","http://10.3.254.34:8080/assist/api/index/nga")
    if toolname=='laohusdk':
        pagehtml=pagetemplate.replace("{PAGEURL}","http://10.3.254.34:8080/assist/api/index/laohu")
    if toolname=='memcache':
        pagehtml=pagetemplate.replace("{PAGEURL}","http://10.3.254.34:8080/assist/api/index/memcache")
    if toolname=='gerenator':
        pagehtml=pagetemplate.replace("{PAGEURL}","http://10.3.254.34:8080/assist/api/index/gerenator")
    if toolname=='tgbus':
        pagehtml=pagetemplate.replace("{PAGEURL}","http://10.3.254.34:8080/assist/api/index/tgbus")
    if toolname=='a9vg':
        pagehtml=pagetemplate.replace("{PAGEURL}","http://10.3.254.34:8080/assist/api/index/a9vg")
    if toolname=='krlaohusdk':
        pagehtml=pagetemplate.replace("{PAGEURL}","http://10.3.254.34:8080/assist/api/index/korean")
    return HttpResponse(pagehtml)
    


    