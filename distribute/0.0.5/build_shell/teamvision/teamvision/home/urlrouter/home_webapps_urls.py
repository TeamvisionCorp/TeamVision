#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from teamvision.home.views.home_webapps_view import all,get_webapp_page,create,delete


webapps_router =[url(r"webapps/(all)$",all),
                 url(r"webapps/get_webapp_page$",get_webapp_page),
                 url(r"webapps/create$",create),
                 url(r"webapps/remove",delete),
                 ]
