#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from doraemon.ci.views import ci_task_view,ci_task_history_view

history_router =[
              url(r"history/(\d{1,9})/download_package$",ci_task_view.download_package),
              url(r"history/(\d{1,9})/package.ipa",ci_task_view.download_package),
              url(r"history/(\d{1,9})/package_list$",ci_task_view.download_package_list),
              url(r"history/buildlog/(\d{1,9})$",ci_task_history_view.get_build_log),
#               url(r"history/log_content/(\d{1,9})",ci_task_history_view.build_log_content),
              url(r"history/download_package/mobile",ci_task_view.mobile_download_page),
#               url(r"history/package/(\d{1,9})/plist",ci_task_view.package_plist),
              url(r"history/download_package/qrcode",ci_task_view.qr_code),
              url(r"history/(\d{1,9})/changelog_detail/([a-z0-9A-Z]*)",ci_task_history_view.changelog_detail),
              url(r"task/(\d{1,9})/more_history",ci_task_view.more_history_list),
              url(r"task/(\d{1,9})/more_changelog",ci_task_view.more_changelog_list),
                ]
