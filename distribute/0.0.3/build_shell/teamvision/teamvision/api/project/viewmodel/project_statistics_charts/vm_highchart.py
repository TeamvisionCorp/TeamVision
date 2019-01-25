#coding=utf-8
'''
Created on 2018-01-09

@author: zhangtiande
'''

from json.encoder import JSONEncoder

class VM_HighChart(object):
    '''
    classdocs
    '''

    def __init__(self,project_id,version_id):
        '''
        Constructor
        '''
        self.chart_id=0
        self.project_id=project_id
        self.version_id=version_id


        