#coding=utf-8
'''
Created on 2018-01-09

@author: zhangtiande
'''

from json.encoder import JSONEncoder
from teamvision.api.project.viewmodel.project_statistics_charts.vm_highchart import VM_HighChart

class VM_PieChart(VM_HighChart):
    '''
    classdocs
    '''

    def __init__(self,project_id,version_id):
        '''
        Constructor
        '''
        VM_HighChart.__init__(VM_PieChart,project_id,version_id)
        self.chart_id=0
        self.project_id=project_id
        self.version_id=version_id
        self.chart_type = 'pie'
        self.show_legend = True
        self.series_name = ''
        self.series_data = list()


        