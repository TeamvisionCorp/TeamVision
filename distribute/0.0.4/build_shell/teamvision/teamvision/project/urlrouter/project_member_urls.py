#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from teamvision.project.views.project_member_view import add,import_member,remove,update_member_role,get_member_list
from teamvision.project.views import project_member_view

member_router=[url(r"^(\d{1,6})/settings/member/add$",add),
               url(r"^(\d{1,6})/settings/member/import",import_member),
              url(r"^(\d{1,6})/settings/member/remove$",remove),
              url(r"^(\d{1,6})/settings/member/add_dialog",project_member_view.get_member_add_dialog),
              url(r"^(\d{1,6})/member/project_member_dropdownlist$",project_member_view.member_dropdownlist),
              url(r"^(\d{1,6})/settings/member/(\d{1,6})/update_role$",update_member_role),
              url(r"^(\d{1,6})/settings/member/get_member_list$",get_member_list),
                 ]