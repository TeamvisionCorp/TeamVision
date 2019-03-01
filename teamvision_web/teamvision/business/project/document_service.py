#coding=utf-8
'''
Created on 2016-10-25

@author: zhangtiande
'''

from teamvision.home.models import FileInfo
from business.business_service import BusinessService
from business.common.file_info_service import FileInfoService
from gatesidelib.common.simplelogger import SimpleLogger
from teamvision.project.models import ProjectDocument
from teamvision.project.mongo_models import  ProjectDocumentMongoFile,ProjectExcelDocumentMongoFile
from django.contrib.admin.models import DELETION, CHANGE, ADDITION


class DocumentService(BusinessService):
    '''
    classdocs
    '''


    @staticmethod
    def create_document(validate_data,user):
        document = ProjectDocument()
        document.Owner = user.id
        document.Parent = validate_data.get("Parent",None)
        document.ProjectID = validate_data.get("ProjectID",0)
        document.ReadOnly = False
        document.Type = validate_data.get("Type",0)
        document_name = validate_data.get("FileName",'新建文件')
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
        pass

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
    def log_create_activity(user, target,target_title):
        ProjectDocument.objects.log_action(user.id, target.id, target_title, ADDITION, "创建了新文档", target.ProjectID)

    @staticmethod
    def log_delete_activity(user, target,target_title):
        ProjectDocument.objects.log_action(user.id, target.id, target_title, DELETION, "删除了文档", target.ProjectID)

    @staticmethod
    def log_change_activity(user, target,target_title):
        ProjectDocument.objects.log_action(user.id, target.id, target_title, CHANGE, "修改了文档", target.ProjectID)




