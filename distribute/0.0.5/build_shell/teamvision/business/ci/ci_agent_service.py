#coding=utf-8
'''
Created on 2015-10-23

@author: zhangtiande
'''
from gatesidelib.common.simplelogger import SimpleLogger
from django.contrib.admin.models import DELETION,CHANGE,ADDITION
from teamvision.home.models import Agent
from teamvision.project.models import  TagOwner
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
    def create_ci_agent(agent_data,user):
        ci_agent = Agent()
        ci_agent = CIAgentService.init_ci_agent(agent_data, ci_agent)
        ci_agent.IsActive = 1
        ci_agent.Creator= user.id
        ci_agent.Status=1
        ci_agent.save()
        agent_tags = agent_data.get('AgentTags',[])
        CIAgentService.create_agent_tag(agent_tags,ci_agent.id)
        CIAgentService.log_create_activity(user, ci_agent)
        return ci_agent
    
    
    
    @staticmethod
    def edit_ci_agent(agent_data,agent_id,user):
        ci_agent=Agent.objects.get(int(agent_id))
        ci_agent=CIAgentService.init_ci_agent(agent_data, ci_agent)
        ci_agent.save()
        agent_tags = agent_data.get('AgentTags', [])
        CIAgentService.create_agent_tag(agent_tags, ci_agent.id)
        CIAgentService.log_change_activity(user, ci_agent)
        return ci_agent
    
    @staticmethod
    def delete_ci_agent(request,server_id):
        ci_agent=Agent.objects.get(int(server_id))
        ci_agent.IsActive=0
        ci_agent.save()
        CIAgentService.log_delete_activity(request.user, ci_agent)
        return ci_agent
            
    

    @staticmethod
    def init_ci_agent(agent_data,ci_agent):
        tmp_ci_agent=ci_agent
        tmp_ci_agent.Name=agent_data.get('Name')
        tmp_ci_agent.AgentWorkSpace=agent_data.get('AgentWorkSpace',"")
        tmp_ci_agent.Executors=agent_data.get('Executors',1)
        tmp_ci_agent.BuildToolsDir=agent_data.get('BuildToolsDir')
        return tmp_ci_agent


    @staticmethod
    def create_agent_tag(tag_ids,agent_id):
        agent_tags = TagOwner.objects.get_tags(agent_id,3)
        for agent_tag in agent_tags:
            if agent_tag.TagID not in tag_ids:
                agent_tag.delete()
        for tag_id in tag_ids:
            tmp_tag_owner = TagOwner.objects.get_tag_byid(agent_id,int(tag_id))
            if len(tmp_tag_owner) == 0:
                tmp_tag_owner = TagOwner()
                tmp_tag_owner.Owner = agent_id
                tmp_tag_owner.OwnerType = 3
                tmp_tag_owner.TagID = tag_id
                tmp_tag_owner.save()



        
    
        
        
    

        
    

    @staticmethod
    def log_create_activity(user,ci_agent):
        Agent.objects.log_action(user.id,ci_agent.id,ci_agent.Name,ADDITION,"创建了新服务",0,CIAgentService.ActionLogType.CI)
    
    @staticmethod
    def log_delete_activity(user,ci_agent):
        Agent.objects.log_action(user.id,ci_agent.id,ci_agent.Name,DELETION,"删除了服务",0,CIAgentService.ActionLogType.CI)
    
    @staticmethod
    def log_change_activity(user,ci_agent):
        Agent.objects.log_action(user.id,ci_agent.id,ci_agent.Name,CHANGE,"修改了服务",0,CIAgentService.ActionLogType.CI)
        
        
        
        