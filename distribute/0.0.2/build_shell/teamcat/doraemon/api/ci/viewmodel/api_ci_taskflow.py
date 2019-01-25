#coding=utf-8
'''
Created on 2016-8-24

@author: zhangtiande
'''
from business.auth_user.user_service import UserService
from doraemon.ci.models import CITaskFlow,CITaskFlowSection

class ApiCITaskFlow(CITaskFlow):
    '''
    classdocs
    '''


    def __init__(self,task_flow):
        '''
        Constructor
        '''
        self.Sections = CITaskFlowSection.objects.flow_sections(task_flow.id)
        