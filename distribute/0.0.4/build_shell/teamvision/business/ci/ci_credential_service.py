#coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''
import platform
from gatesidelib.common.simplelogger import SimpleLogger
from gatesidelib.common.commonhelper import CommonHelper
from gatesidelib.common.aes_encrypt_hepler import AESEncrypt

from django.contrib.admin.models import DELETION,CHANGE,ADDITION
from teamvision.ci.models import CICredentials
from itertools import chain
from business.business_service import BusinessService


class CICredentialService(BusinessService):
    '''
    classdocs
    '''
    
    @staticmethod
    def get_all_credentials(request):
        public_credentials=CICredentials.objects.get_public_credentials()
        my_credentials=CICredentials.objects.get_my_credentials(request.user.id).exclude(Scope=1)
        return chain(public_credentials,my_credentials)
    
    
    @staticmethod
    def create_ci_credential(request):
        ci_credential=CICredentials()
        ci_credential=CICredentialService.init_ci_credential(request, ci_credential)
        ci_credential.IsActive=1
        ci_credential.Creator=request.user.id
        ci_credential.save()
        CICredentialService.log_create_activity(request.user, ci_credential)
        return ci_credential
    
    
    
    @staticmethod
    def edit_ci_credential(request):
        credential_id=request.POST.get("CredentialID")
        ci_credential=CICredentials.objects.get(int(credential_id))
        ci_credential=CICredentialService.init_ci_credential(request, ci_credential)
        ci_credential.save()
        CICredentialService.log_change_activity(request.user, ci_credential)
        return ci_credential
    
    @staticmethod
    def delete_ci_credential(request,credential_id):
        ci_credential=CICredentials.objects.get(int(credential_id))
        ci_credential.IsActive=0
        ci_credential.save()
        CICredentialService.log_delete_activity(request.user, ci_credential)
        return ci_credential
            
    

    @staticmethod
    def init_ci_credential(request,ci_credential):
        tmp_ci_credential=ci_credential
        tmp_ci_credential.UserName=request.POST.get('UserName')
        tmp_ci_credential.CredentialType=request.POST.get('CredentialType')
        tmp_ci_credential.Description=request.POST.get('Description',"")
        password=request.POST.get('Password')
        if not CommonHelper.is_windows():
            encrpyter=AESEncrypt("Hsbjiademlsdftu9")
            password=encrpyter.encrypt(password)
        tmp_ci_credential.Password=password
        tmp_ci_credential.Scope=request.POST.get('Scope')
        tmp_ci_credential.SSHKey=request.POST.get('SSHKey')
        return tmp_ci_credential
    
    
    
    
        

    @staticmethod
    def log_create_activity(user,ci_credential):
        CICredentials.objects.log_action(user.id,ci_credential.id,ci_credential.UserName,ADDITION,"创建了证书",-1,CICredentialService.ActionLogType.CI)
    
    @staticmethod
    def log_delete_activity(user,ci_credential):
        CICredentials.objects.log_action(user.id,ci_credential.id,ci_credential.UserName,DELETION,"删除了证书",-1,CICredentialService.ActionLogType.CI)
    
    @staticmethod
    def log_change_activity(user,ci_credential):
        CICredentials.objects.log_action(user.id,ci_credential.id,ci_credential.UserName,CHANGE,"修改了证书",-1,CICredentialService.ActionLogType.CI)
        
        
        
        