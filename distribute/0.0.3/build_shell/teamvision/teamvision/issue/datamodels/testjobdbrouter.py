#coding=utf-8
#!encoding=utf-8
'''
Created on 2013-12-30

@author: ETHAN
'''

class TestJobDBRouter(object):
    '''
    db router for testjob
    '''
    def db_for_read(self,model,**hints):
        ''' read data from db testjob
        '''
        if model._meta.app_label=='testjob':
            return 'testjob'
    
    def db_for_write(self,model,**hints):
        ''' write data to db testjob
        '''
        if model._meta.app_label=='testjob':
            return 'testjob'
    
    def allow_syncdb(self,db,model):
        ''' make sure doraemon.testjob just in db dorameon_testjob
        '''
        if db=='testjob':
            return model._meta.app_label=="testjob"
        elif model._meta.app_label=="testjob":
            return False
        
    def allwo_relation(self,obj1,obj2,**hints):
        if obj1._meta.app_label == 'testjob' or obj2._meta.app_label == 'testjob':
            return True
        return None