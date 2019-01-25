#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.ci.views.ci_settings_view import settings_agent,settings_global_variable,credential_edit_page,credential_edit
from doraemon.ci.views.ci_settings_view import  settings_credentials,credential_create,credential_delete
from doraemon.ci.views.ci_settings_view import  server_edit_page,server_delete,settings_server,server_create,server_edit
from doraemon.ci.views import ci_settings_view  


settings_router =[
                url(r"settings/(agent)$",settings_agent),
                url(r"settings/agent/(\d{1,3})/create_dialog",ci_settings_view.agent_create_dialog),
                url(r"settings/agent/(\d{1,3})/create",ci_settings_view.agent_create),
                url(r"settings/(tags)$",ci_settings_view.settings_tag),
                url(r"settings/tag/(\d{1,3})/create",ci_settings_view.task_tag_create),
                url(r"settings/(credentials)$",settings_credentials),
                url(r"settings/credentials/credential_create$",credential_create),
                url(r"settings/credentials/credential_edit$",credential_edit),
                url(r"settings/(global_variable)$",settings_global_variable),
                url(r"settings/credentials/(\d{1,9})/edit_page$",credential_edit_page),
                url(r"settings/credentials/(\d{1,9})/delete$",credential_delete),
                
                url(r"settings/servers/(\d{1,9})/edit_page$",server_edit_page),
                url(r"settings/servers/(\d{1,9})/delete$",server_delete),
                url(r"settings/(servers)$",settings_server),
                url(r"settings/servers/server_create$",server_create),
                url(r"settings/servers/server_edit$",server_edit),
                ]
