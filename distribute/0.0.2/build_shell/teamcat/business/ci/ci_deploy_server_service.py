#coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''
from gatesidelib.common.simplelogger import SimpleLogger
from django.contrib.admin.models import DELETION,CHANGE,ADDITION
from doraemon.ci.models import CIServer
from business.business_service import BusinessService


class CIDeployServerService(BusinessService):
    '''
    classdocs
    '''
    
    @staticmethod
    def get_all_servers(request):
        return CIServer.objects.all()
    
    
    @staticmethod
    def create_ci_server(request):
        ci_server=CIServer()
        ci_server=CIDeployServerService.init_ci_server(request, ci_server)
        ci_server.IsActive=1
        ci_server.Creator=request.user.id
        ci_server.save()
        CIDeployServerService.log_create_activity(request.user, ci_server)
        return ci_server
    
    
    
    @staticmethod
    def edit_ci_server(request):
        server_id=request.POST.get("ServerID")
        ci_server=CIServer.objects.get(int(server_id))
        ci_server=CIDeployServerService.init_ci_server(request, ci_server)
        ci_server.save()
        CIDeployServerService.log_change_activity(request.user, ci_server)
        return ci_server
    
    @staticmethod
    def delete_ci_server(request,server_id):
        ci_server=CIServer.objects.get(int(server_id))
        ci_server.IsActive=0
        ci_server.save()
        CIDeployServerService.log_delete_activity(request.user, ci_server)
        return ci_server
            
    

    @staticmethod
    def init_ci_server(request,ci_server):
        tmp_ci_server=ci_server
        tmp_ci_server.ServerName=request.POST.get('ServerName')
        tmp_ci_server.Credential=request.POST.get('Credential')
        tmp_ci_server.Description=request.POST.get('Description',"")
        tmp_ci_server.Port=request.POST.get('Port',0)
        tmp_ci_server.RemoteDir=request.POST.get('RemoteDir',"")
        tmp_ci_server.Scope=request.POST.get('Scope',1)
        tmp_ci_server.Host=request.POST.get('Host',"")
        return tmp_ci_server
    
    
    
    
        

    @staticmethod
    def log_create_activity(user,ci_server):
        CIServer.objects.log_action(user.id,ci_server.id,ci_server.ServerName,ADDITION,"添加服务器",-1,CIDeployServerService.ActionLogType.CI)
    
    @staticmethod
    def log_delete_activity(user,ci_server):
        CIServer.objects.log_action(user.id,ci_server.id,ci_server.ServerName,DELETION,"删除了服务器",-1,CIDeployServerService.ActionLogType.CI)
    
    @staticmethod
    def log_change_activity(user,ci_server):
        CIServer.objects.log_action(user.id,ci_server.id,ci_server.ServerName,CHANGE,"修改了服务器",-1,CIDeployServerService.ActionLogType.CI)