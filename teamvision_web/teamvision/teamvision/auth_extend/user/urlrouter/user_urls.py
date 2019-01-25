#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from django.conf.urls import url
from teamvision.auth_extend.user.views.auth_extend_user_view import login,logout

urlpatterns =[url(r"^login$",login),
              url(r"^logout$",logout)
                 ]