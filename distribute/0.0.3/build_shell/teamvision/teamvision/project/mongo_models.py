# coding=utf-8
'''
Created on 2017年9月4日

@author: ethan
'''
from model_managers.mongo_model.mongo_model_manager import MongoFileManager
from model_managers.mongo_model.mongo_model import MongoFile
from teamvision.settings import MONGODB
from mongoengine import *
import datetime

connect(db=MONGODB['default']['DB'], alias=MONGODB['default']['ALIAS'], port=MONGODB['default']['PORT'],
        host=MONGODB['default']['HOST'])


class FortestingMongoFile(MongoFile):
    HOST = MONGODB['project_documents']['HOST']
    PORT = MONGODB['project_documents']['PORT']
    DB = MONGODB['project_documents']['DB']
    objects = MongoFileManager(HOST, PORT, DB, "fortesting_doc")


class IssueMongoFile(MongoFile):
    HOST = MONGODB['project_issue']['HOST']
    PORT = MONGODB['project_issue']['PORT']
    DB = MONGODB['project_issue']['DB']
    objects = MongoFileManager(HOST, PORT, DB, "issue_attachment")


class ReportMongoModel(Document):
    meta = {'abstract': True, 'db_alias': MONGODB['default']['ALIAS']}
    is_active = BooleanField(default=True)
    create_time = DateTimeField(default=datetime.datetime.now())

class Feature(EmbeddedDocument):
    id = StringField(required=False,null=True)
    Content = StringField(required=True)
    Passed1 = BooleanField(default=False)
    Passed2 = BooleanField(default=False)
    Passed3 = BooleanField(default=False)


class TestingProgress(EmbeddedDocument):
    Progress = StringField(required=True)
    BugSummary = StringField()
    Feature = ListField(EmbeddedDocumentField(Feature))


class ProjectSummary(EmbeddedDocument):
    Project = StringField(required=True)
    Version = StringField()
    Tester = StringField()
    Dev = StringField()
    PM = StringField()
    StartDate = StringField()


class ReleaseNotification(EmbeddedDocument):
    Title = StringField(required=True)
    Tester = StringField(required=False)
    Project = StringField()
    Progress = StringField()
    ReleaseDate = StringField()
    QA = StringField(required=False)
    FE = StringField(required=False)
    PM = StringField(required=False)
    Service = StringField(required=False)
    Client = StringField(required=False)
    Data = StringField(required=False)

class BugAttachment(EmbeddedDocument):
    name = StringField(required=False,null=True)
    url = StringField(required=False,null=True)


class TestingReport(ReportMongoModel):
    meta = {'abstract': True, 'db_alias': MONGODB['default']['ALIAS']}
    FortestingID = IntField(required=True)
    ReportType = IntField(required=True)
    Recipients = ListField(IntField())
    CCList = StringField(required=False,null=True)
    Topic = StringField(required=True)
    ProjectInfo = EmbeddedDocumentField(ProjectSummary)
    FeatureProgress = EmbeddedDocumentField(TestingProgress)
    Comments = StringField(required=False,null=True)
    BugTrendAttachments = ListField(EmbeddedDocumentField(BugAttachment))


class BVTReport(TestingReport):
    BVTDetailResult = StringField(max_length=500, required=False)
    BVTVerdict = StringField(max_length=500, required=True)


class TestProgressReport(TestingReport):
    pass


class TestingCompleteReport(TestingReport):
        ReleaseNotification = EmbeddedDocumentField(ReleaseNotification)
