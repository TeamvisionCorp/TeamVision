#coding=utf-8
'''
Created on 2015-12-25

@author: Devuser
'''
from pymongo import MongoClient
from gridfs  import GridFS,GridFSBucket
from bson import ObjectId

class MongodbHelper(object):
    '''
    classdocs
    '''
    
    def __init__(self,host,port):
        self.host=host
        self.port=port
    
    def save(self,database,collection,value):
        client=MongoClient(self.host,self.port)
        db=client[database]
        collection=db[collection]
        return collection.save(value)
    
    def remove(self,database,collection,doc_id):
        client=MongoClient(self.host,self.port)
        db=client[database]
        collection=db[collection]
        return collection.remove(doc_id)
    
    def get(self,database,collection,doc_id):
        client=MongoClient(self.host,self.port)
        db=client[database]
        collection=db[collection]
        return collection.find_one({'_id':ObjectId(doc_id)})

    def put_file(self,database,collection,file_byte,file_name,file_real_name,content_type):
        client=MongoClient(self.host,self.port)
        db=client[database]
        file_fs=GridFS(db)
        id=file_fs.put(file_byte,filename=file_name,name=file_real_name,content_type=content_type)
        return id
    
    def pub_file_bucket(self,database,collection,file_name,file_property):
        client=MongoClient(self.host,self.port)
        db=client[database]
        bucket_files=GridFSBucket(db,bucket_name=collection)
        file_bucket_fs=bucket_files.open_upload_stream(filename=file_name,metadata=file_property)
        return file_bucket_fs
    
    def delete_file(self,database,collection,file_id):
        client=MongoClient(self.host,self.port)
        db=client[database]
        bucket_files=GridFSBucket(db,bucket_name=collection)
        bucket_files.delete(ObjectId(file_id))
        client.close()
    
    def get_file_bucket(self,database,collection,file_id):
        client=MongoClient(self.host,self.port)
        db=client[database]
        bucket_files=GridFSBucket(db,bucket_name=collection)
        grid_out =bucket_files.open_download_stream(ObjectId(file_id))
        client.close()
        return grid_out
        