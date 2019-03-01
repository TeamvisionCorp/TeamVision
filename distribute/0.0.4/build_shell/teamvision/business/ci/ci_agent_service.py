#coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''
from gatesidelib.common.simplelogger import SimpleLogger
from django.contrib.admin.models import DELETION,CHANGE,ADDITION
from teamvision.home.models import Agent
from business.business_service import BusinessService


class CIAgentService(BusinessService):
    '''
    classdocs
    '''
    
    @staticmethod
    def get_all_agents():
        return Agent.objects.all()
    
    
    @staticmethod
    def update_agent_status(request):
        agent_id=int(request.GET.get("agent_id",0))
        status=request.GET.get("status",3)
        agent=Agent.objects.get(agent_id)
        agent.Status=int(status)
        agent.save()
    
    
    @staticmethod
    def create_ci_agent(request):
        ci_agent=Agent()
        ci_agent=CIAgentService.init_ci_agent(request, ci_agent)
        ci_agent.IsActive=1
        ci_agent.Creator=request.user.id
        ci_agent.Status=1
        ci_agent.save()
        CIAgentService.log_create_activity(request.user, ci_agent)
        return ci_agent
    
    
    
    @staticmethod
    def edit_ci_agent(request,agent_id):
        ci_agent=Agent.objects.get(int(agent_id))
        ci_agent=CIAgentService.init_ci_agent(request, ci_agent)
        ci_agent.save()
        CIAgentService.log_change_activity(request.user, ci_agent)
        return ci_agent
    
    @staticmethod
    def delete_ci_agent(request,server_id):
        ci_agent=Agent.objects.get(int(server_id))
        ci_agent.IsActive=0
        ci_agent.save()
        CIAgentService.log_delete_activity(request.user, ci_agent)
        return ci_agent
            
    

    @staticmethod
    def init_ci_agent(request,ci_agent):
        print(request.POST)
        tmp_ci_agent=ci_agent
        tmp_ci_agent.Name=request.POST.get('Name')
        tmp_ci_agent.IP=request.POST.get('IP')
        tmp_ci_agent.OS=request.POST.get('OS')
        tmp_ci_agent.AgentPort=request.POST.get('AgentPort',0)
        tmp_ci_agent.AgentWorkSpace=request.POST.get('AgentWorkSpace',"")
        tmp_ci_agent.AgentTags=request.POST.get('AgentTags',"0,")+","
        tmp_ci_agent.Executors=request.POST.get('Executors',1)
        tmp_ci_agent.BuildToolsDir=request.POST.get('BuildToolsDir')
        return tmp_ci_agent
        
    
        
        
    

        
    

    @staticmethod
    def log_create_activity(user,ci_agent):
        Agent.objects.log_action(user.id,ci_agent.id,ci_agent.Name,ADDITION,"创建了新服务",0,CIAgentService.ActionLogType.CI)
    
    @staticmethod
    def log_delete_activity(user,ci_agent):
        Agent.objects.log_action(user.id,ci_agent.id,ci_agent.Name,DELETION,"删除了服务",0,CIAgentService.ActionLogType.CI)
    
    @staticmethod
    def log_change_activity(user,ci_agent):
        Agent.objects.log_action(user.id,ci_agent.id,ci_agent.Name,CHANGE,"修改了服务",0,CIAgentService.ActionLogType.CI)
        
        
        
        