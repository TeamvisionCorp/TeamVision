#coding=utf-8
'''
Created on 2015-11-17

@author: zhangtiande
'''

from teamvision.user_center.mongo_models import UCenterMongoFile
from teamvision.project.mongo_models import TempFileMongoFile
from teamvision.home.models import FileInfo
from business.common.file_info_service import FileInfoService
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
    def store_cached_file(cached_file_keys):
        result = list()
        keys = cached_file_keys
        for key in keys:
            if key != "":
                temp_file = TempFileMongoFile.objects.get(key)
                if temp_file is not None:
                    mongo_id = UCenterMongoFile.objects.copy_bucket(temp_file)
                    file_id = FileInfoService.add_file(0, mongo_id, temp_file.metadata['file_real_name'], 1, 0,
                                                       temp_file.length)
                    TempFileMongoFile.objects.delete_file(key)
                    if file_id != 0:
                        result.append(file_id)
        return result

    @staticmethod
    def cache_issue_attachments(upload_file, user):
        message = {"cache_key": "", "message": "上传文件超过10M"}
        try:
            if AccountService.validate_upload_file(upload_file, 10 * 1024 * 1024, None):
                mongo_id = MongoDBService.save_file(upload_file, TempFileMongoFile)
                message["cache_key"] = str(mongo_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
            message["message"] = str(ex)
        return message


    @staticmethod
    def download_attachment(file_id,mongo_model):
        return FileInfoService.get_file(int(file_id), mongo_model)

    @staticmethod
    def delete_attachment(file_id, user_id):
        FileInfoService.delete_file(int(file_id), mongo_model=UCenterMongoFile)

    @staticmethod
    def delete_tempfile(file_id):
        TempFileMongoFile.objects.delete_file(file_id)

        
    
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
                        result="/api/ucenter/profiles/download_file/"+str(avatar)
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
    def get_file_suffixes(file_name):
        length=len(file_name.split('.'))
        file_suffixes=file_name.split('.')[length-1]
        return file_suffixes


    @staticmethod
    def validate_upload_file(upload_file,size,file_type):
        '''
        upload_file: request.Files['upload_file']
        size: file size int
        file_type: ['png','jpg'] list
        '''
        result=False
        file_content_type=AccountService.get_file_suffixes(upload_file.name)
        if upload_file.size<=size:
            result=True
        if file_type!=None:
            if result and  file_content_type in file_type:
                result=True
            else:
                result=False
        return result



    @staticmethod
    def update_avatar(user,cached_file_keys):
        file_list = AccountService.store_cached_file(cached_file_keys)
        if len(file_list) > 0:
            if user.extend_info.avatar.isnumeric():
                FileInfoService.delete_file(int(user.extend_info.avatar), mongo_model=UCenterMongoFile)
                user.extend_info.avatar = file_list[0]
                user.extend_info.save()
            else:
                user.extend_info.avatar = file_list[0]
                user.extend_info.save()
        return AccountService.get_avatar_url(user,)

                
            
        
        
        
        
        
        
        
                                                                               
                                                                               
            
            
        
        
        