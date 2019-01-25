#coding=utf-8
#!encoding=utf-8
'''
Created on 2013-12-30

@author: ETHAN
'''

class AutomationTaskDBRouter(object):
    '''
    db router for automationtesting
    '''
    def db_for_read(self,model,**hints):
        ''' read data from db automationtask
        '''
        if model._meta.app_label=='automationtesting':
            return 'automationtesting'
    
    def db_for_write(self,model,**hints):
        ''' write data to db automationtask
        '''
        if model._meta.app_label=='automationtesting':
            return 'automationtesting'
    
    def allow_syncdb(self,db,model):
        ''' make sure doraemon.automationtask just in db dorameon_automationtask
        '''
        if db=='automationtesting':
            return model._meta.app_label=="automationtesting"
        elif model._meta.app_label=="automationtesting":
            return False
        
    def allwo_relation(self,obj1,obj2,**hints):
        if obj1._meta.app_label == 'automationtesting' or obj2._meta.app_label == 'automationtesting':
            return True
        
        return None