#coding=utf-8
# coding=utf-8
'''
Created on 2014-3-18

@author: ETHAN
'''

from django.shortcuts import render_to_response

def loadleftnavigater(request):
    ''' load left navigater'''
    return render_to_response("common/leftnavigater.html")