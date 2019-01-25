#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.project.views.project_fortesting_view import all,edit,edit_page,get_create_dialog,create,download
from doraemon.project.views import project_fortesting_view


fortesting_router=[url(r"(\d{1,6})/fortesting/(all)",all),url(r"(\d{1,6})/fortesting/(\d{1,6})$",edit_page),url(r"(\d{1,6})/fortesting/(\d{1,6})/edit$",edit),
                   url(r"fortesting/get_create$",get_create_dialog),
                   url(r"fortesting/get_confirm_dialog$",project_fortesting_view.get_confirm_dialog),
                   url(r"fortesting/(\d{1,10})/edit$",edit),
                   url(r"fortesting/create$",create),
                   url(r"fortesting/(\d{1,6})/update_status/(\d{1,6})$",project_fortesting_view.update_status),
                   url(r"fortesting/download/(\d{1,10})$",download),
                   url(r"fortesting/(\d{1,10})/project_module_list$",project_fortesting_view.get_module_list),
                   url(r"fortesting/(\d{1,10})/project_version_list$",project_fortesting_view.get_version_list),
                   url(r"fortesting/(\d{1,10})/project_member_list$",project_fortesting_view.get_member_list),
                   url(r"fortesting/(\d{1,10})/fortesting_items/(\d{1,10})$",project_fortesting_view.get_column_items),
                   url(r"fortesting/upload_attachment$",project_fortesting_view.upload_file),
                   url(r"fortesting/(\d{1,10})/delete_file/(\d{1,10})$",project_fortesting_view.delete_file),
                   url(r"fortesting/(\d{1,10})/add_tester/(\d{1,10})$",project_fortesting_view.add_tester),
                   url(r"fortesting/(\d{1,10})/remove_tester/(\d{1,10})$",project_fortesting_view.remove_tester),
                   url(r"fortesting/(\d{1,10})/view_part/(\d{1,10})$",project_fortesting_view.get_fortesting_view_part),
                   url(r"fortesting/download_attachment/(\d{1,10})$",project_fortesting_view.download_attachment),
                   url(r"fortesting/(\d{1,10})/update_testingdate$",project_fortesting_view.update_testingdate),
                ]