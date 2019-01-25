#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.project.views.project_webhook_view import add,edit,remove,perform,web_hook,set_default

webhook_router=[url(r"^(\d{1,6})/settings/webhook/create$",add),
              url(r"^(\d{1,6})/settings/webhook/(\d{1,6})/remove$",remove),
              url(r"^(\d{1,6})/webhook/(\d{1,6})/edit$",edit),
              url(r"^(\d{1,6})/settings/webhook/(\d{1,6})/set_default$",set_default),
              url(r"^(\d{1,6})/settings/webhook/(\d{1,6})/perform$",perform),
              url(r"^(\d{1,6})/settings/(webhook)$",web_hook),
              url(r"webhook/(\d{1,6})/perform$",perform)
                 ]