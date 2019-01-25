#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.ci.views.ci_service_view import index,create,config,config_post,upload_file,download_file
from doraemon.ci.views import ci_service_view 


service_router =[
              url(r"service/(all)",index),
              url(r"service/product/(\d{1,4})$",index),
              url(r"service/create",create),
              url(r"service/(\d{1,9})/config_post",config_post),
              url(r"service/(\d{1,9})/replace_config_post",ci_service_view.replace_config_post),
              url(r"service/(\d{1,9})/config",config),
              url(r"service/(\d{1,9})/upload_file",upload_file),
              url(r"service/(\d{1,9})/copy",ci_service_view.copy),
              url(r"service/(\d{1,9})/delete",ci_service_view.delete),
              url(r"service/product/(\d{1,4})/service_list$",ci_service_view.service_list),
              url(r"service/download_file/(\d{1,10})$",download_file),
              url(r"service/delete_file/(\d{1,9})$",ci_service_view.delete_file),
              
                ]
