#coding=utf-8
#!encoding=utf-8
'''
Created on 2013-12-30

@author: ETHAN
'''

class ProductQualityDBRouter(object):
    '''
    db router for productquality
    '''
    def db_for_read(self,model,**hints):
        ''' read data from db productquality
        '''
        if model._meta.app_label=='productquality':
            return 'productquality'
    
    def db_for_write(self,model,**hints):
        ''' write data to db productquality
        '''
        if model._meta.app_label=='productquality':
            return 'productquality'
    
    def allow_syncdb(self,db,model):
        ''' make sure doraemon.productquality just in db dorameon_productquality
        '''
        if db=='productquality':
            return model._meta.app_label=="productquality"
        elif model._meta.app_label=="productquality":
            return False
        
    def allwo_relation(self,obj1,obj2,**hints):
        if obj1._meta.app_label == 'productquality' or obj2._meta.app_label == 'productquality':
            return True
        return None