#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from django import forms
class TestTaskForm(forms.Form):
    '''
    Test task form model
    '''
    def __init__(self,customizeParameters,*args, **kwargs):
        super(TestTaskForm, self).__init__(*args, **kwargs)
        self.fields['TaskBrowsers'].choices=customizeParameters['browsers']
        self.fields['TaskMachineID'].choices=customizeParameters['machines']
        self.fields['TaskProjectID'].choices=customizeParameters['projects']
        self.fields['TaskTestingConfigID'].choices=customizeParameters['testingconfigs']
    
    id=forms.CharField(widget=forms.HiddenInput,initial=0,required=False)
    TaskName=forms.CharField()
    TaskTestingConfigID=forms.ChoiceField(choices=[],initial=0)
    TaskCaseSetID=forms.IntegerField(required=False)
    TaskDependentTaskID=forms.IntegerField(required=False)
    TaskDependencyRuleID=forms.IntegerField(required=False)
    TaskBrowsers=forms.MultipleChoiceField(required=False, choices=[])
    TaskIsMonitored=forms.BooleanField(initial=False,required=False)
    TaskMachineID=forms.ChoiceField(choices=[],required=False)
    TaskProjectID=forms.ChoiceField(choices=[],required=False)
    TaskIsSplit=forms.BooleanField(initial=False,required=False)
#     def setavaliableTCF(self,value):
#         self.avaliableTCF=value
#     
#     def setavaliableBrowsers(self,value):
#         self.avaliableBrowsers=value
#         
#     def setavaliableMachines(self,value):
#         self.avaliableMachines=value
#     
#     def setavaliableProjects(self,value):
#         self.avaliableProjects=value
#     
    