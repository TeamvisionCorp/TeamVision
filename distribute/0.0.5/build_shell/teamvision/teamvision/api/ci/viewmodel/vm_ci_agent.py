#coding=utf-8
'''
Created on 2016-7-6

@author: zhangtiande
'''

from teamvision.home.models import Agent


class VM_CIAgent(object):
    '''
    classdocs
    '''


    def __init__(self,agent_id):
        '''
        Constructor
        '''
        self.agent_id=int(agent_id)
        self.agent_name=self.get_agent().Name
        self.agent_port=self.get_agent().AgentPort
        self.agent_workspace=self.get_agent().AgentWorkSpace
    
    def get_agent(self):
        agent=Agent.objects.get(self.agent_id)
        if agent==None:
            raise Exception("agent not exists with id "+str(self.agent_id))
        return agent
        
    
    
   
    
    
    
                
        