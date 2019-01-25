#coding=utf-8
'''
Created on 2015-11-4

@author: Devuser
'''

from teamvision.ci.models import CITask
from business.auth_user.user_service import UserService
from teamvision.home.models import FileInfo
from business.common.system_config_service import SystemConfigService
from teamvision.settings import WEB_HOST

class VM_CIBuildFile(object):
    '''
    classdocs
    '''
    
    def __init__(self,file_id,hisotry_id):
        self.file_id=file_id
        self.file=FileInfo.objects.get(self.file_id)
        self.history_id=hisotry_id
    
    
    def file_name(self):
        return self.file.FileName
    
    def download_uri(self):
        return "/ci/history/"+str(self.file_id)+"/download_package"
        
    def file_icon(self):
        result="default.png"
        if self.file.FileSuffixes in SystemConfigService.get_file_type_white_list():
            result=self.file.FileSuffixes+".png"
        return "/static/global/images/file_types/"+result
    def qrcode_uri(self):
        result=""
        if "APK" in self.file_name().upper() or "IPA" in self.file_name().upper():
            result= WEB_HOST+"/ci/history/download_package/mobile?package="+self.download_uri()+"&file_id="+str(self.file_id)+"&history_id="+str(self.history_id)
        return result