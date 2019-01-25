#coding=utf-8
'''
Created on 2014-10-22

@author: zhangtiande
'''
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib import auth


def login(request):
    username = request.GET.get('user', '')
    password = request.GET.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        # Redirect to a success page.
        return HttpResponseRedirect("/testjob/testsubmition/index")
    else:
        # Show an error page
        return HttpResponseRedirect("/testjob/testsubmition/create")