#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from doraemon.ci.pagefactory.ci_plugin_pageworker import CIPluginPageWorker
from gatesidelib.common.simplelogger import SimpleLogger



@login_required
def get_plugin(request,section_id):
    ''' index page'''
    try:
        page_worker=CIPluginPageWorker(request)
        plugin_id=request.GET.get("plugin_id")
        result=page_worker.get_plugin(None,int(plugin_id))
    except Exception as ex:
        SimpleLogger.exception(ex)
    return HttpResponse(result)
    


    