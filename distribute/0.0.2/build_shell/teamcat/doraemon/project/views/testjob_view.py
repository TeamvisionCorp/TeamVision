#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from doraemon.home.viewmodels.vm_home import VM_Home


class menuitem(object):
    
    def __init__(self,namevalue,keyvalue):
        self.key=keyvalue
        self.name=namevalue
    
    def get_name(self):
        return self.name
    
    def get_key(self):
        return self.key
    
    def get_id(self):
        return "123456"
        

@login_required
def index_list(request):
    ''' index page'''
    vm_myplace=VM_Home(request.user)
    return render_to_response('testjob/home_testjob_index.html',{'request':vm_myplace},context_instance=RequestContext(request))

def load_leftnavigater(request):
    try:
        menuitemlist=list()
        item=menuitem("缺陷","fa fa-bug fa-fw")
        item1=menuitem("用例","fa fa-leaf fa-fw")
        menuitemlist.append(item)
        menuitemlist.append(item1)
#         menuitemlist.append(item)
        testjob_active="leftmeunactive"
        return render_to_response('home/home_index_left_nav.html',{'meunitemlist':menuitemlist,'testjob_active':testjob_active},context_instance=RequestContext(request))
    except Exception as ex:
        print(ex)
        
def load_left_sub_navigater(request):
    try:
        return render_to_response('testjob/home_testjob_leftsub_nav.html',context_instance=RequestContext(request))
    except Exception as ex:
        print(ex)

def load_testjob_list(request):
    try:
        return render_to_response('testjob/home_testjob_listview.html',context_instance=RequestContext(request))
    except Exception as ex:
        print(ex)

def load_content_activity(request):
    try:
        return render_to_response('dash_board/home_dashboard_activity.html',context_instance=RequestContext(request))
    except Exception as ex:
        print(ex)
    
    
    
    
    


    