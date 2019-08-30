#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''

from django.conf.urls import url
from teamvision.api.ucenter.views import user_profilesview


api_user_profiles_router =[
                  url(r"profiles/update_avatar",user_profilesview.UCenterProfilesAvatarView.as_view()),
                  url(r"profiles/download_file/((?P<file_id>.+))",user_profilesview.UCenterProfilesAvatarView.as_view()),
                  url(r"profiles/clear_tempfiles/((?P<file_id>.+))",user_profilesview.UCenterProfilesAvatarView.as_view()),
                  url(r"attachment/upload$",user_profilesview.UCenterUploadView.as_view()),
                  ]
