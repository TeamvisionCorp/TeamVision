#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from teamvision.project.views.project_version_view import all,create,delete,update_version,update_date

version_router=[url(r"(\d{1,6})/version$",all),
                url(r"(\d{1,6})/version/create$",create),
                url(r"(\d{1,6})/version/(\d{1,6})/delete",delete),
                url(r"(\d{1,6})/version/(\d{1,6})/update_version$",update_version),
                url(r"(\d{1,6})/version/(\d{1,6})/update_date$",update_date)]