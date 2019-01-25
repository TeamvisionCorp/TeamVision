#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.project.views.project_settings_view import basic,member,get_create_dialog,create,edit,delete,check_value_exists
from doraemon.project.views import project_settings_view

settings_router=[url(r"^(\d{1,6})/settings/(basic)$",basic),
                 url(r"^(\d{1,6})/settings/(version)$",basic),
                 url(r"^(\d{1,6})/settings/(module)$",basic),
                 url(r"^(\d{1,6})/settings/(member)$",member),
                 url(r"(\d{1,6})/settings/version/create$",project_settings_view.create_version),
                url(r"(\d{1,6})/settings/version/(\d{1,6})/delete",project_settings_view.delete_version),
                url(r"(\d{1,6})/settings/version/(\d{1,6})/update_version$",project_settings_view.update_version),
                url(r"(\d{1,6})/settings/version/(\d{1,6})/update_date$",project_settings_view.update_date),
                 url(r"(\d{1,6})/settings/module/create$",project_settings_view.create_module),
                url(r"(\d{1,6})/settings/module/(\d{1,6})/delete",project_settings_view.delete_module),
                url(r"(\d{1,6})/settings/module/(\d{1,6})/update_name$",project_settings_view.update_module),
                url(r"(\d{1,6})/settings/module/(\d{1,6})/update_desc$",project_settings_view.update_module),
                 url(r"^create_dialog$",get_create_dialog),
                 url(r"^create$",create),
                 url(r"^create$",create),
                 url(r"^(\d{1,6})/settings/basic/edit$",edit),
                 url(r"^(\d{1,6})/settings/basic/delete$",delete),
                 url(r"^check_value_exists$",check_value_exists),
                 
                 ]