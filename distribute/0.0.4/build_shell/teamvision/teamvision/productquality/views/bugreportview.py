#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from django.shortcuts import render_to_response,render,HttpResponse

from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from business.productquality.codequalityservice import CodeQualityService
from business.productquality.bugreportservice import BugReportService
from gatesidelib.common.simplelogger import SimpleLogger

@login_required
def index_list(request):
    ''' index page'''
    return render_to_response('bugreport/bugreportindex.html',context_instance=RequestContext(request))


def load_leftcontainer(request):
    ''' load left container '''
    return render_to_response('bugreport/bugreportleftcontainer.html',context_instance=RequestContext(request))

def load_chartcontainer(request):
    ''' load chart container '''
    return render_to_response('bugreport/bugreportchart.html',context_instance=RequestContext(request))

def get_productname_control(request):
    platformid=request.POST['platformid']
    result=CodeQualityService.get_productname_control(platformid)
    return HttpResponse(result)

def get_productversion(request):
    result=CodeQualityService.get_productversion_control(request.POST['productid'],request.POST['platformid'])
    return HttpResponse(result)

def get_perday_bugcounts_data(request):
    try:
        submitionid=request.GET['submitionid']
        SimpleLogger.logger.info("get_perday_data with submitionid "+submitionid)
        perday_bugcounts_data=BugReportService.get_perday_bugcounts_data(submitionid)
        SimpleLogger.logger.info("return data  "+str(perday_bugcounts_data))
    except Exception as ex:
        SimpleLogger.logger.info(ex.message)
    return HttpResponse(perday_bugcounts_data)

def get_allday_bugcounts_data(request):
    submitionid=request.GET['submitionid']
    all_bugcounts_data=BugReportService.get_all_bugcounts_data(submitionid)   
    return HttpResponse(all_bugcounts_data)
    
    