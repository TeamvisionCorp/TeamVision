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
from gatesidelib.common.simplelogger import SimpleLogger

@login_required
def index_list(request):
    ''' index page'''
    return render_to_response('codequality/codequalityindex.html',context_instance=RequestContext(request))


def load_leftcontainer(request):
    ''' load left container '''
    return render_to_response('codequality/codequalityleftcontainer.html',context_instance=RequestContext(request))

def get_productname_control(request):
    platformid=request.POST['platformid']
    result=CodeQualityService.get_productname_control(platformid)
    return HttpResponse(result)

def get_productversion(request):
    result=CodeQualityService.get_productversion_control(request.POST['productid'],request.POST['platformid'])
    return HttpResponse(result)

def get_productcodelines(request):
    submitionid=request.GET['submitionid']
    codelines=CodeQualityService.get_developer_newcodelines(submitionid)
    return HttpResponse(codelines)

def get_productbugs(request):
    submitionid=request.GET['submitionid']
    bugcountsforeveryversion=CodeQualityService.get_bugs_everyversion(submitionid)   
    return HttpResponse(bugcountsforeveryversion.replace("u",""))

def get_productbug_rates(request):
    submitionid=request.GET['submitionid']
    bugrates=CodeQualityService.get_product_bugrates(submitionid)
    SimpleLogger.logger.info(bugrates)
    return HttpResponse(bugrates)



def get_chart(request):
    submitionid=request.POST['submitionid']
    if int(submitionid):
        return render(request,'codequality/codequalitychart.html')
    else:
        return render(request,'codequality/codequalityhome.html')
    

    
    