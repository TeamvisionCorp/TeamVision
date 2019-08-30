#coding=utf-8
'''
Created on 2016-10-25

@author: zhangtiande
'''

from teamvision.home.models import FileInfo
from business.business_service import BusinessService
from business.common.file_info_service import FileInfoService
from teamvision.project.mongo_models import TempFileMongoFile,ProjectDocumentMongoFile
from gatesidelib.common.simplelogger import SimpleLogger
from business.common.mongodb_service import MongoDBService
from teamvision.project.models import ProjectDocument
from teamvision.project.mongo_models import  ProjectDocumentMongoFile,ProjectExcelDocumentMongoFile
from django.contrib.admin.models import DELETION, CHANGE, ADDITION


class DocumentService(BusinessService):
    '''
    classdocs
    '''


    @staticmethod
    def create_document(validate_data,user,create_file=True):
        document = ProjectDocument()
        document.Owner = user.id
        document.Parent = validate_data.get("Parent",None)
        document.ProjectID = validate_data.get("ProjectID",0)
        document.ReadOnly = False
        document.Type = validate_data.get("Type",0)
        document.FileID = 0
        document_name = validate_data.get("FileName",'新建文件')

        if create_file:
            file_id = FileInfoService.add_file(document.Parent,'',document_name,document.Type,user.id,0)
            document.FileID = file_id
        document.save()
        DocumentService.log_create_activity(user,document,document_name)
        return document

    @staticmethod
    def delete_document(document_id,user):
        document = ProjectDocument.objects.get(int(document_id))
        document_name = '--'
        file_info = FileInfo.objects.get(document.FileID)
        if file_info:
            document_name = file_info.FileName
        if document.Type == 1:
            child_documents = ProjectDocument.objects.get_child_documents(document.id)
            if len(child_documents)>0:
                DocumentService.delete_child_document(child_documents)
                document.delete()
            else:
                file_info = FileInfo.objects.get(document.FileID)
                file_info.delete()
                document.delete()
        if document.Type == 2:
            file_info = FileInfo.objects.get(document.FileID)
            FileInfoService.delete_value(file_info.id, ProjectExcelDocumentMongoFile)
            document.delete()
        if document.Type == 3:
            file_info = FileInfo.objects.get(document.FileID)
            FileInfoService.delete_value(file_info.id, ProjectDocumentMongoFile)
            document.delete()
        DocumentService.log_delete_activity(user,document,document_name)

    @staticmethod
    def delete_child_document(child_documents):
        for document in child_documents:
            if document.Type == 1:
                childs = ProjectDocument.objects.get_child_documents(document.id)
                if len(childs)>0:
                    DocumentService.delete_child_document(childs)
                    document.delete()
                else:
                    file_info = FileInfo.objects.get(document.FileID)
                    file_info.delete()
                    document.delete()
            if document.Type == 2:
                file_info = FileInfo.objects.get(document.FileID)
                FileInfoService.delete_value(file_info.id,ProjectExcelDocumentMongoFile)
                document.delete()
            if document.Type == 3:
                file_info = FileInfo.objects.get(document.FileID)
                FileInfoService.delete_value(file_info.id,ProjectDocumentMongoFile)
                document.delete()
        return 0


    @staticmethod
    def save_content_tomongo(content,file):
        excel_mongo_file = ProjectExcelDocumentMongoFile()
        if file.FilePath is not None and file.FilePath != "":
            excel_mongo_file.objects.update_value(file.FilePath,{"excel_content":content})
        else:
            mongo_id = excel_mongo_file.objects.save_value({"excel_content":content})
            file.FilePath = mongo_id
        file.save()

    @staticmethod
    def store_cached_file(cached_file_keys,project_id,parent,user):
        result = list()
        keys = cached_file_keys
        for key in keys:
            if key != "":
                temp_file = TempFileMongoFile.objects.get(key)
                if temp_file != None:
                    mongo_id = ProjectDocumentMongoFile .objects.copy_bucket(temp_file)
                    valid_data = dict()
                    if str(parent) == "":
                        valid_data['Parent'] = None
                    else:
                        valid_data['Parent'] = parent
                    valid_data['ProjectID'] = project_id
                    valid_data['Type'] = 3
                    valid_data['FileName'] = temp_file.metadata['file_real_name']
                    print(1)
                    file_id = FileInfoService.add_file(0, mongo_id, temp_file.metadata['file_real_name'], 1, 0,
                                                       temp_file.length)
                    print(file_id)
                    document = DocumentService.create_document(valid_data,user,False)
                    document.FileID = file_id
                    document.save()
                    TempFileMongoFile.objects.delete_file(key)
                    result.append(document.id)
        return result

    @staticmethod
    def cache_upload_document(upload_file, user):
        message = {"cache_key": "", "message": "上传文件超过20M"}
        try:
            if DocumentService.validate_upload_file(upload_file, 20 * 1024 * 1024, None):
                mongo_id = MongoDBService.save_file(upload_file, TempFileMongoFile)
                message["cache_key"] = str(mongo_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
            message["message"] = str(ex)
        return message

    @staticmethod
    def download_document(file_id):
        if file_id.isnumeric():
            document = ProjectDocument.objects.get(int(file_id))
            temp_file = FileInfoService.get_file(int(document.FileID), ProjectDocumentMongoFile)
        else:
            temp_file = TempFileMongoFile.objects.get(file_id)
        return temp_file


    @staticmethod
    def delete_cache_document(mongo_id):
        ProjectDocumentMongoFile.objects.delete_file(mongo_id)




    @staticmethod
    def log_create_activity(user, target,target_title):
        ProjectDocument.objects.log_action(user.id, target.id, target_title, ADDITION, "创建了新文档", target.ProjectID)

    @staticmethod
    def log_delete_activity(user, target,target_title):
        ProjectDocument.objects.log_action(user.id, target.id, target_title, DELETION, "删除了文档", target.ProjectID)

    @staticmethod
    def log_change_activity(user, target,target_title):
        ProjectDocument.objects.log_action(user.id, target.id, target_title, CHANGE, "修改了文档", target.ProjectID)




