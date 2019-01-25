#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from django.conf.urls import url
from doraemon.administrate.views.admin_device_view import all,device_create_get,device_create_post,device_edit_get,device_edit_post,get_version_controll

from doraemon.administrate.views.admin_device_view import borrow_device,lend_device,return_device,get_devcie_confirm_dialog,device_delete
admin_device_router=[
                    url(r"device/(all)$",all),
                    url(r"device/(lending)$",all),
                    url(r"device/(android)$",all),
                    url(r"device/(ios)$",all),
                    url(r"device/(other)$",all),
                    url(r"device/create$",device_create_get),
                    url(r"device/create_post$",device_create_post),
                    url(r"device/edit/(\d{1,3})$",device_edit_get),
                    url(r"device/edit_post$",device_edit_post),
                    url(r"device/borrow$",borrow_device),
                    url(r"device/lend$",lend_device),
                    url(r"device/return$",return_device),
                    url(r"device/confirm_dialog$",get_devcie_confirm_dialog),
                    url(r"device/delete$",device_delete),
                    url(r"device/version_controll",get_version_controll),
                    
                 ]