# coding=utf-8
'''
Created on 2014-11-2

@author: Zhangtiande
'''

from business.business_service import BusinessService
from business.common.file_info_service import FileInfoService
from business.common.mongodb_service import MongoDBService


class UploadFileService(BusinessService):
    @staticmethod
    def attachments_upload_handler(file):
        message = ""
        mongo_file_id = UploadFileService.save_to_mongo(file)
        file_id = FileInfoService.add_file(0, mongo_file_id, file.name, 1, 0, file.size)
        if file_id != 0:
            message = str(file_id)
        return message

    @staticmethod
    def download_attachment(mongo_model, file_path):
        return mongo_model.objects.get(file_path)

    @staticmethod
    def delete_file(file_id, mongo_model):
        FileInfoService.delete_file(file_id, mongo_model)

    @staticmethod
    def save_to_mongo(file, size, mongo_model):
        result = 0
        upload_file = file
        if UploadFileService.validate_upload_file(upload_file, size, None):
            result = MongoDBService.save_file(upload_file, mongo_model)
        return result
