package com.xracoon.teamcat.agent.app;

import java.lang.Thread.UncaughtExceptionHandler;

import org.apache.log4j.Logger;

public class AgentTerminateExceptionHandler implements UncaughtExceptionHandler {

	private Logger logger=Logger.getLogger(AgentTerminateExceptionHandler.class);
	
	public Agent agent;
	public AgentTerminateExceptionHandler(Agent agent)
	{
		this.agent=agent;
	}
	
	@Override
	public void uncaughtException(Thread t, Throwable e) 
	{
		logger.error("Exception in Thread: "+t.getId());
		logger.error(e.getMessage(), e);
		agent.shutdown();
	}
}
