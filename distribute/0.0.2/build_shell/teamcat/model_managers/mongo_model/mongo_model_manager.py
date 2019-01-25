#coding=utf-8
'''
Created on 2015-10-22

@author: zhangtiande
'''


from gatesidelib.mongodb_helper import MongodbHelper
from doraemon.gatesidelib.common.simplelogger import SimpleLogger


class MongoFileManager(object):
    
    def __init__(self,host,port,db,collection):
        self.host=host
        self.port=port
        self.collection=collection
        self.db=db
        self.default_db="doraemon"
        self.default_collection="ci"
    
    def get(self,file_id):
        mongo_helper=MongodbHelper(self.host,self.port)
        grid_out=mongo_helper.get_file_bucket(self.db, self.collection, file_id)
        if grid_out==None:
            grid_out=mongo_helper.get_file_bucket(self.default_db, self.default_collection, file_id)
        return grid_out
        
    
    def get_by_filename(self,file_name):
        pass
    
    def save(self,file_bytes,file_property):
        mongo_helper=MongodbHelper(self.host,self.port)
        file_id=mongo_helper.put_file(self.db,self.collection,file_bytes,file_property)
        return file_id
    
    def delete_file(self,file_id):
        try:
            mongo_helper=MongodbHelper(self.host,self.port)
            mongo_helper.delete_file(self.db,self.collection, file_id)
            mongo_helper.delete_file(self.default_db,self.default_collection, file_id)
        except Exception as ex:
            SimpleLogger.exception(ex)
    
    def delete_value(self,file_id):
        mongo_helper=MongodbHelper(self.host,self.port)
        file_id=mongo_helper.remove(self.db,self.collection, file_id)
        file_id=mongo_helper.remove(self.default_db,self.default_collection, file_id)
        return file_id
    
    def save_bucket(self,file_chunks,file_name,file_property):
        mongo_helper=MongodbHelper(self.host,self.port)
        file_bucket_fs=mongo_helper.pub_file_bucket(self.db,self.collection,file_name,file_property)
        for chunk in file_chunks:
            file_bucket_fs.write(chunk)
        file_bucket_fs.close()
        return file_bucket_fs._id
    
    def copy_bucket(self,grid_out):
        mongo_helper=MongodbHelper(self.host,self.port)
        file_bucket_fs=mongo_helper.pub_file_bucket(self.db,self.collection,grid_out.name,grid_out.metadata)
        print(grid_out.length)
        while True:
            chunk=grid_out.read(size=1024*1024*10)
            print(len(chunk))
            if chunk:
                file_bucket_fs.write(chunk)
            else:
                break
        file_bucket_fs.close()
        print(file_bucket_fs._id)
        return file_bucket_fs._id
        

    def save_content(self,content,file_name,file_property):
        mongo_helper=MongodbHelper(self.host,self.port)
        file_bucket_fs=mongo_helper.pub_file_bucket(self.db,self.collection,file_name,file_property)
        file_bucket_fs.write(content.encode(encoding="utf-8"))
        file_bucket_fs.close()
        return file_bucket_fs._id
        
    

    
