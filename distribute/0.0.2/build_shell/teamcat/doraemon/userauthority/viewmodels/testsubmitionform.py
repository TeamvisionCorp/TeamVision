#coding=utf-8
# coding=utf-8
'''
Created on 2014-1-5

@author: ETHAN
'''
from django import forms
class TestSubmitionForm(forms.Form):
    '''
    Test task form model
    '''
    def __init__(self,customizeParameters,*args, **kwargs):
        super(TestSubmitionForm, self).__init__(*args, **kwargs)
        self.fields['TPSProductName'].choices=customizeParameters['TPSProductName']
        self.fields['TPSProductType'].choices=customizeParameters['TPSProductType']
        self.fields['TPSDevelopers'].choices=customizeParameters['TPSDevelopers']
        self.fields['TPSStatus'].choices=customizeParameters['TPSStatus']
        self.fields['TPSSubmiter'].choices=customizeParameters['TPSSubmiter']
        self.fields['TPSCC'].choices=customizeParameters['TPSCC']
        self.fields['TPSPlatform'].choices=customizeParameters['TPSPlatform']
        self.fields['TPSJenkinsServer'].choices=customizeParameters['TPSJenkinsServer']
        self.fields['TPSJenkinsJobName'].choices=customizeParameters['TPSJenkinsJobName']

    
    
    id=forms.CharField(widget=forms.HiddenInput,initial=0,required=False)
    TPSProductName=forms.ChoiceField(choices=[],required=True)
    TPSProductType=forms.ChoiceField(choices=[],initial=0)
    TPSPlatform=forms.ChoiceField(choices=[],initial=0,required=True)
    TPSProductVersion=forms.CharField(required=True)
    TPSDevelopers=forms.MultipleChoiceField(choices=[],required=True)
    TPSSubmiter=forms.ChoiceField(choices=[],required=True)
    TPSStatus=forms.ChoiceField(required=False, choices=[])
    TPSCC=forms.MultipleChoiceField(choices=[],required=False)
    TPSCodeVersion=forms.CharField(required=True)
    TPSCodeUrl=forms.CharField(required=True)
    TPSFunctionChange=forms.CharField(required=True,widget=forms.Textarea)
    TPSBugFix=forms.CharField(required=True,widget=forms.Textarea)
    TPSAdvice4Testing=forms.CharField(required=True,widget=forms.Textarea)
    TPSPackageAddress=forms.CharField(required=True)
    TPSJenkinsJobName=forms.ChoiceField(choices=[],required=False)
    TPSJenkinsServer=forms.ChoiceField(choices=[],required=False)
    