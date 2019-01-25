#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.project.views import project_archive_view

archive_router=[url(r"^(\d{1,6})/archive/(all)$",project_archive_view.index),
                url(r"^(\d{1,6})/archive/(\d{1,6})$",project_archive_view.archive_file),
                url(r"^archive/download/(\d{1,6})$",project_archive_view.download_package),
                 ]