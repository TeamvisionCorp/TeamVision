#coding=utf-8
'''
Created on 2015-11-17

@author: zhangtiande
'''

from doraemon.user_center.mongo_models import UCenterMongoFile
from doraemon.home.models import FileInfo
from business.common.mongodb_service import MongoDBService
from gatesidelib.common.simplelogger import SimpleLogger

class AccountService(object):
    '''
    classdocs
    '''
    
    @staticmethod
    def avatar_upload_handler(request):
        message=""
        file_id=AccountService.save_to_mongo(request)
        if file_id!=0:
            message=str(file_id)
        return message
        
    
    @staticmethod
    def get_avatar_file(request,mongo_file_id):
        return UCenterMongoFile.objects.get(mongo_file_id)
    
    @staticmethod
    def get_avatar_url(user):
        result=""
        try:
            if user.extend_info:
                avatar=user.extend_info.avatar
                if avatar:
                    if avatar.startswith("/static"):
                        result=avatar
                    else:
                        mongo_file_id=FileInfo.objects.get(int(avatar)).FilePath
                        result="/ucenter/account/get_avatar/"+mongo_file_id
        except Exception as ex:
            SimpleLogger.exception(ex)
        return result
    
    @staticmethod
    def save_to_mongo(request):
        result=0
        upload_file=request.FILES['avatar_file']
        if AccountService.validate_upload_file(upload_file):
            result=MongoDBService.save_file(upload_file,UCenterMongoFile)
        return result
    
    @staticmethod
    def add_file(request,folder_id,file_mongo_id,file_name,file_size):
        file_info=FileInfo()
        file_info.FileCreator=request.user.id
        file_info.FileFolder=folder_id
        file_info.FileName=file_name
        file_info.FilePath=file_mongo_id
        file_info.FileSuffixes=AccountService.get_file_suffixes(file_name)
        file_info.FileType=1
        file_info.FileSize=(file_size/1024)+1
        return file_info
    
    
    @staticmethod
    def get_file_suffixes(file_name):
        length=len(file_name.split('.'))
        file_suffixes=file_name.split('.')[length-1]
        return file_suffixes
    
    @staticmethod
    def validate_upload_file(upload_file):
        result=False
        file_content_type=AccountService.get_file_suffixes(upload_file.name)
        if upload_file.size<=10*1024*1024:
            result=True
        else:
            result=False
        if result and  file_content_type in ["png","jpg","jpeg"]:
            result=True
        else:
            result=False
        return result
    
    @staticmethod
    def update_avatar(request):
        avatar=request.POST.get("avatar")
        if avatar:
            if avatar.startswith("/static"):
                request.user.extend_info.avatar=avatar
                request.user.extend_info.save()
            else:
                url_list=avatar.split("/")
                mongo_file_id=url_list[len(url_list)-1]
                mongo_file=UCenterMongoFile.objects.get(mongo_file_id)
                file_name=mongo_file.metadata['file_real_name']
                file_info=AccountService.add_file(request,0,mongo_file_id,file_name,mongo_file.length)
                file_info.save()
                request.user.extend_info.avatar=file_info.id
                request.user.extend_info.save()
    
    @staticmethod
    def update_user_info(request):
        current_user=request.user
        current_user.first_name=request.POST.get("first_name")
        current_user.last_name=request.POST.get("last_name")
        current_user.email=request.POST.get("email")
        current_user.save()
                
            
        
        
        
        
        
        
        
                                                                               
                                                                               
            
            
        
        
        