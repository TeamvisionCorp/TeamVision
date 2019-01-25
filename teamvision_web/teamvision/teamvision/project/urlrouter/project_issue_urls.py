#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from teamvision.project.views import project_issue_view

issue_router=[url(r"^(\d{1,9})/issue/(all)$",project_issue_view.index),
              url(r"^(\d{1,9})/issue/(\d{1,9})$",project_issue_view.index),
              url(r"^(\d{1,9})/issue/list$",project_issue_view.get_issue_list),
              url(r"^(\d{1,9})/issue/list_more/(\d{1,9})$",project_issue_view.get_issue_more),
              url(r"^issue/open_create_dialog$",project_issue_view.get_create_dialog),
              url(r"^issue/cached_attachment$",project_issue_view.cached_file),
              url(r"^issue/download/(\d{1,10})$",project_issue_view.download_file),
              url(r"^issue/delete_file/(\d{1,10})$",project_issue_view.delete_file),
              url(r"^issue/cached_attachment/remove$",project_issue_view.remove_cache),
               url(r"^issue/(\d{1,9})/cached_attachment/save$",project_issue_view.save_cache),
              url(r"^issue/(\d{1,9})/detail$",project_issue_view.get_issue_detail),
              url(r"^issue/(\d{1,9})/([a-zA-Z]{5,20})/(\d{1,3})$",project_issue_view.update_issue),
              url(r"^issue/(\d{1,9})/update$",project_issue_view.update_issue),
              url(r"^issue/(\d{1,9})/comments/add$",project_issue_view.add_comment),
              url(r"^(\d{1,9})/issue/export$",project_issue_view.export_issue_result),
              url(r"^issue/(\d{1,9})/attachment/(\d{1,9})/view$",project_issue_view.attachment_view),
              url(r"^issue/attachment/(\d{1,9})/view_iframe$",project_issue_view.attachment_view_iframe),
              url(r"^issue/(\d{1,9})/open_upload_file_dialog$",project_issue_view.get_upload_dialog),
              url(r"^issue/(\d{1,9})/open_issue_operation_dialog/(\d{1,3})$",project_issue_view.get_issue_operation_dialog),
              url(r"^issue/(\d{1,9})/save_issue_operation_result/(\d{1,3})$",project_issue_view.update_issue_operation_result),
              url(r"^issue/create$",project_issue_view.create_issue),
              url(r"^(\d{1,9})/issue_filter/(\d{1,9})/save_dialog",project_issue_view.get_issue_filter_save_dialog),
              url(r"^(\d{1,9})/issue_filter/(\d{1,9})/create",project_issue_view.create_issue_filter),
              url(r"^issue_filter/get_list",project_issue_view.get_issue_filter_list),
              url(r"^(\d{1,9})/issue/filter/(\d{1,9})/cache$",project_issue_view.cache_issue_filter),
              url(r"^(\d{1,9})/issue/search/cache$",project_issue_view.cache_issue_search_word),
              url(r"^issue/filter/clean$",project_issue_view.clean_issue_filter),
              url(r"^issue/filter/(\d{1,9})/filter_ui_config$",project_issue_view.filter_ui_config),
              url(r"^issue/filter/(\d{1,9})/filter_panel$",project_issue_view.get_issue_filter_panel),
              url(r"^issue/filter/(\d{1,9})/filter_panel$",project_issue_view.get_issue_filter_panel),
                 ]