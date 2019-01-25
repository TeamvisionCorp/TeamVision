# coding=utf-8
'''
Created on 2017年9月4日

@author: ethan
'''
from model_managers.mongo_model.mongo_model_manager import MongoFileManager
from model_managers.mongo_model.mongo_model import MongoFile
from doraemon.settings import MONGODB


class MockAPIMongoFile(MongoFile):
    HOST = MONGODB['env_mock']['HOST']
    PORT = MONGODB['env_mock']['PORT']
    DB = MONGODB['env_mock']['DB']
    objects = MongoFileManager(HOST, PORT, DB, "mock_handler")