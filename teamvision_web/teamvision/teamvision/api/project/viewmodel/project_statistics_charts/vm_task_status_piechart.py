#coding=utf-8
'''
Created on 2018-01-09

@author: zhangtiande
'''

from business.common.system_config_service import SystemConfigService
from teamvision.api.project.viewmodel.project_statistics_charts.vm_piechart import VM_PieChart
from business.project.task_statistics_service import TaskStatisticsService

class VM_TaskStatusPieChart(VM_PieChart):
    '''
    classdocs
    '''

    def __init__(self,project_id,version_id,request):
        '''
        Constructor
        '''
        VM_PieChart.__init__(VM_TaskStatusPieChart,project_id,version_id)
        self.chart_id=0
        self.project_id=project_id
        self.version_id=version_id
        self.request = request
        self.chart_type = 'pie'
        self.chart_title = '任务状态'
        self.show_legend = True
        self.series_name = '任务占比'
        self.series_data = self.get_series_data()


    def get_series_data(self):
        result =list()
        status_data = TaskStatisticsService.task_count_bystatus(self.project_id,self.version_id,self.request)
        for data_item in status_data:
            temp_dict = dict()
            temp_dict['name'] = SystemConfigService.get_dic_data_name('ProjectTaskStatus',data_item.get('Status'))
            temp_dict['y'] = data_item.get('TotalCount')
            result.append(temp_dict)
        return result



        