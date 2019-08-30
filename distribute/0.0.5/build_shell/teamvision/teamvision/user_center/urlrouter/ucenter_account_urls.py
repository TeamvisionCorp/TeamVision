#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: zhangtiande
'''
from django.conf.urls import url
from teamvision.user_center.views.ucenter_account_view import basic,password,upload_avatar,avatar,avatar_file,update_avatar,update_user_info,change_password

account_router=[url(r"^(\d{1,6})/account/(basic)$",basic),
                    url(r"^(\d{1,6})/account/(password)$",password),
                    url(r"^(\d{1,6})/account/upload_avatar$",upload_avatar),
                    url(r"^(\d{1,6})/account/avatar$",avatar),
                    url(r"^account/get_avatar/([a-z0-9A-Z_]{24,24})",avatar_file),
                    url(r"account/update_avatar$",update_avatar),
                    url(r"account/update_user_info",update_user_info), 
                    url(r"account/change_password",change_password),
                 ]