package com.xracoon.teamcat.agent.taskrun;

import java.util.Date;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.xracoon.teamcat.agent.config.TeamcatAppender;
import com.xracoon.teamcat.driver.TaskInfo;
import com.xracoon.util.basekit.hudson.proc.Proc;

public class RunnerInfo {
	public Logger logger=LoggerFactory.getLogger(RunnerInfo.class);
	public DriverRunner runner;
	public boolean forceStop;
	
	public TaskInfo task;
	public boolean isTimeout;
	public Date stopStart;
	
	public TeamcatAppender dappender;
}
