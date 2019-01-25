package com.xracoon.teamcat.agent.taskrun;

import java.io.File;
import java.util.Date;
import java.util.LinkedHashMap;
import java.util.Map;
import org.apache.log4j.FileAppender;
import org.apache.log4j.Level;
import org.apache.log4j.PatternLayout;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.xracoon.teamcat.agent.app.Agent;
import com.xracoon.teamcat.agent.app.Messages;
import com.xracoon.teamcat.agent.config.AgentConfig;
import com.xracoon.teamcat.agent.config.TeamcatAppender;
import com.xracoon.teamcat.agent.device.Device;
import com.xracoon.teamcat.agent.webservice.AgentWebService;
import com.xracoon.teamcat.driver.DatasEnum;
import com.xracoon.teamcat.driver.TaskInfo;
import com.xracoon.teamcat.driver.WebService;
import com.xracoon.util.basekit.system.OS;

/**
 * 任务执行线程
 * @author Yangtianxin
 */
public class TaskExecutor extends Thread {
	
	private Logger logger = LoggerFactory.getLogger(TaskExecutor.class);
	private Map<Long, RunnerInfo> taskMap=new LinkedHashMap<Long, RunnerInfo>();
	
	private AgentConfig agentConfig;
	private Agent agent;
	
	public TaskExecutor(Agent agent)
	{
		super(agent,"TaskDispatchThread");
		this.agent=agent;
		this.agentConfig=agent.getAgentConfig();
	}
	
	public String queryTaskState()
	{
		RunnerInfo[] infos=null;
		synchronized(this){
			infos=taskMap.values().toArray(new RunnerInfo[0]);
		}
		StringBuilder builder=new StringBuilder();
		builder.append("TaskState in queue:  "+infos.length+" task"+(infos.length>1?"s":"")+" is running\n");
		for(RunnerInfo ri: infos)
		{
			builder.append("[taskID="+ri.task.taskID+",  taskName="+ri.task.taskConfig.getTaskName()+",  taskQueueId="+ri.task.taskQueueID+"]  " );
			builder.append("assiginRunner="+(ri.runner!=null)+",  forceStop="+ri.forceStop);
//			if(ri.runner!=null)
//				builder.append(",  isAlive="+ri.runner.isAlive()+", rusult="+ri.runner.getResult());
		}
		return builder.toString();
	}
	
	/**
	 * Add task for run
	 * @param taskQueueID
	 * @return  return null when task added successfully; otherwise return error message
	 * @throws Exception 
	 */
	public String addTask(TaskInfo info){
		try {
			//读取任务信息
			WebService.queryTaskConfig(info);
			RunnerInfo[] infos=null;
			synchronized(this){
				infos=taskMap.values().toArray(new RunnerInfo[0]);
			}
			logger.info("task infos ： "+infos.toString());
			if(info.taskType==DatasEnum.AutoTaskType_Interface.getValue() || info.taskType==DatasEnum.AutoTaskType_WebUI.getValue()){
				if(OS.isMac())
					throw new Exception("Can't run interface_test or web_ui_test task on Mac OS (host issues)");
				
				for(RunnerInfo ri: infos)
					if(ri.task.taskType==DatasEnum.AutoTaskType_Interface.getValue() || ri.task.taskType==DatasEnum.AutoTaskType_WebUI.getValue())
						return Messages.taskstart_error_plantRunning;	
			}
			else if(info.taskType==DatasEnum.AutoTaskType_APPUI.getValue()){
				Device dev=agent.getDeviceMonitor().getDevice(info.deviceSNo);
				if(dev==null)
					return Messages.taskstart_error_deviceInavailable+": "+info.deviceSNo;
				
				for(RunnerInfo ri: infos)
					if(ri.task.deviceSNo!=null && ri.task.deviceSNo.equals(info.deviceSNo))
						return Messages.taskstart_error_deviceUsing+": "+info.deviceSNo;	
				
				info.device=dev;
			}
			//Package或Deploy, 任务重复检查
			else{
				for(RunnerInfo ri: infos)
					if(ri.task.taskID == info.taskID)
						return Messages.taskstart_error_sameTaskNotCleaned;
			}
			
			RunnerInfo runInfo=new RunnerInfo();
			runInfo.task=info;
			
			//logger
			TeamcatAppender dapp=new TeamcatAppender(info.taskQueueID, agentConfig.logCacheBatch, agentConfig.logCacheTimeoutSec);
			runInfo.dappender=dapp;
			Logger runlogger=getRunnerLogger(info, dapp);
			if(runlogger!=null)
				runInfo.logger=runlogger;
			else
				logger.warn("get logger for task "+info.taskID+"_"+info.taskQueueID+" failed!");

			synchronized(this){
				taskMap.put(info.taskQueueID,runInfo);
			}
			
			runTask(runInfo);
//			if(info.taskType==DatasEnum.AutoTaskType_Interface.getValue() || info.taskType==DatasEnum.AutoTaskType_WebUI.getValue()
//					|| info.taskType==DatasEnum.AutoTaskType_PACKAGE.getValue() || info.taskType==DatasEnum.AutoTaskType_DEPLOY.getValue()){
//				WebService.agentUpate(agentConfig.agentKey, DatasEnum.AutoAgentStatus_Running.getValue());
//			}
//			else if(info.taskType==DatasEnum.AutoTaskType_APPUI.getValue()){
//				WebService.devUpdate(info.deviceSNo, DatasEnum.MobileDeviceStatus_Running.getValue());
//			}
			
			logger.info("add task:  t"+info.taskID+"("+info.taskConfig.getTaskName()+")_tq"+info.taskQueueID);
			runInfo.logger.info("add task:  t"+info.taskID+"("+info.taskConfig.getTaskName()+")_tq"+info.taskQueueID);
			
			return null;
		}catch (Exception e) {
			logger.error(e.getMessage(), e);
			return "Execption when run task : "+e.getMessage();
		}
	}
	
	public String stopTask(long tqId, boolean isTimeout){
//		resetRunner(taskID);
//		tqs.updateTaskQueueStatus(taskID, DatasDict.TaskInQueueStatus_Aborted);
		
		//adjust RunnerInfo status
		RunnerInfo info=taskMap.get(tqId);
		if(info==null)
			return "Can't find task "+tqId+" in agent "+agentConfig.agentName+" "+agentConfig.agentKey;
		
		boolean ret=false;
		info.forceStop=true;
		info.isTimeout=isTimeout;
		info.stopStart=new Date();
		
		//stop driver process
		try {
			info.runner.proc.kill();
			ret=!info.runner.proc.isAlive();
			
			//remove from queue
			synchronized(this){
				taskMap.remove(info.task.taskQueueID);
			}
			
			//post sync work
			finishTask(info);
			
		} catch (Exception e) {
			logger.error("Exception when kill task process: ", e);
			return "Exception when kill task process: "+e.getMessage();
		}
			
		return ret?null:"Kill failed:　Task process still Alive";
	}
	
	public synchronized void setDriverError(long tqId, String error){
		RunnerInfo info=taskMap.get(tqId);
		if(info!=null)
			info.runner.setRunError(error);
	}

	public void finishTask(RunnerInfo info) throws Exception{
		logger.info("post-precess task ...  t"+info.task.taskID+"("+info.task.taskConfig.getTaskName()+")_tq"+info.task.taskQueueID);
		info.logger.info("post-precess task ...  t"+info.task.taskID+"("+info.task.taskConfig.getTaskName()+")_tq"+info.task.taskQueueID);
		
		DriverRunner runner=info.runner;
		DatasEnum status=DatasEnum.TaskInQueueStatus_Aborted;
		String error=null;
		if(runner!=null){
			Boolean driverStatus=runner.getResult();
			String error0=runner.getErrorMsg();
			
			if(info.forceStop && !info.isTimeout){
				status=DatasEnum.TaskInQueueStatus_Aborted;
				error="Task Stop";
			}
			else if(info.forceStop && info.isTimeout){
				status=DatasEnum.TaskInQueueStatus_Timeout;
				error="Task Timeout";
			}
			else if(driverStatus!=null && driverStatus){
				status=DatasEnum.TaskInQueueStatus_Complete;
				//error="Task Complete";
			}
			else if(driverStatus!=null){
				status=DatasEnum.TaskInQueueStatus_Error;
				error="Task Error";
			}
			
			if(error!=null && error0!=null && error0.trim().length()>0)
				error+=":"+error0;
			
//			if(info.task.taskType==DatasEnum.AutoTaskType_Interface.getValue() || info.task.taskType==DatasEnum.AutoTaskType_WebUI.getValue()
//					|| info.task.taskType==DatasEnum.AutoTaskType_PACKAGE.getValue() || info.task.taskType==DatasEnum.AutoTaskType_DEPLOY.getValue()){
//				WebService.agentUpate(agentConfig.agentKey, DatasEnum.AutoAgentStatus_Online.getValue());
//			}
//			else if(info.task.taskType==DatasEnum.AutoTaskType_APPUI.getValue()){
//				WebService.devUpdate(info.task.deviceSNo, DatasEnum.MobileDeviceStatus_Online.getValue());
//			}
			
			if(!OS.isMac() && info.task.taskType==DatasEnum.AutoTaskType_Interface.getValue() || info.task.taskType==DatasEnum.AutoTaskType_WebUI.getValue()){
				info.logger.info("restore host...");
				OS.getNewInstance().resotreHost("./host.bak");
			}
		}
		
		//clean appender cache
		info.logger.info(info.dappender.getEndTag());
		
		//wait to flush log (1 min)
		logger.info("wait to flush log (60 secondes)...");
		int num=60;
		while(!info.dappender.IsLogDone() && (num--)>0)
			Thread.sleep(1000);
		
		logger.info("tqDone:  driverRunner result: "+">"+status+" : "+error);
		info.logger.info("tqDone:  driverRunner result: "+">"+status+" : "+error);
		
		int ret=AgentWebService.tqDone(info.task.taskQueueID, status.getValue(), (error!=null&&error.length()>200)?error.substring(0, 200)+"...":error);
		logger.info("tqDone result: "+ret);		
		logger.info("===>finish task done: t"+info.task.taskID+"("+info.task.taskConfig.getTaskName()+")_tq"+info.task.taskQueueID);
	}
	
	public String getLogFile(TaskInfo info){
		return "logs/t"+info.taskID+"/t"+info.taskID+"_tq"+info.taskQueueID+".log";
	}
	
	private Logger getRunnerLogger(TaskInfo info, TeamcatAppender dapp){
		try{
			//通过底层Logger API设置
			String loggerName="logger4tq."+info.taskQueueID;
			org.apache.log4j.Logger logger=org.apache.log4j.Logger.getLogger("logger4tq."+info.taskQueueID);
			logger.setAdditivity(false);
			logger.setLevel(Level.INFO);
			logger.removeAllAppenders();
			
			PatternLayout layout = new PatternLayout("[%d] %m");
			try{
				FileAppender fapp=new FileAppender(layout,getLogFile(info),false);
				logger.addAppender(fapp);
			}catch(Exception e){
				logger.warn("failed to create local log file :"+e.getMessage(),e);
			}
//			PatternLayout clayout = new PatternLayout("--[%d - %6p]  %m%n");
//			ConsoleAppender capp=new ConsoleAppender(clayout);
//			logger.addAppender(capp);
			
			dapp.setLayout(new PatternLayout("%m"));
			logger.addAppender(dapp);
			
			//返回门面API
			return LoggerFactory.getLogger(loggerName);
		}catch(Exception e){
			logger.error("create taskRunner logger failed :"+e.getMessage(),e);
			return null;
		}
	}
	
	public void runTask(RunnerInfo info) throws Exception{
		logger.info(">>>executing log for task t"+info.task.taskID+"("+info.task.taskConfig.getTaskName()+")_tq"+info.task.taskQueueID+" redirect into file : "+getLogFile(info.task));
		
		//Thread
//		DriverThreadRunner runner=new DriverThreadRunner(agent.getAgentConfig(), agent.getOS(), info.task);
//		runner.logger=info.logger;
//		info.runner=runner;
//		runner.startDriver();
		
		//Process: 准备数据, 启动进程
		DriverRunner runner=new DriverRunner(agent.getAgentConfig(), agent.getOS(), info.task);
		runner.logger=info.logger;
		info.runner=runner;
		runner.runProcess();
	}
	
	@Override
	public void run() {
		try {
			logger.info("task executor thread started");
			
			File lastScanFile=new File("lastTaskScan");
			if(!lastScanFile.exists())
				lastScanFile.createNewFile();
			
			while(true){
				
				RunnerInfo[] infos=null;
				synchronized(this){
					infos=taskMap.values().toArray(new RunnerInfo[0]);
				}
				
				//清理正常结束的任务
				for(RunnerInfo ri: infos){
					if(ri.runner!=null && ri.runner.proc!=null &&!ri.runner.proc.isAlive()){
						synchronized(this){
							taskMap.remove(ri.task.taskQueueID);
						}
						finishTask(ri);
					}
				}
				
				lastScanFile.setLastModified(new Date().getTime());
				Thread.sleep(agentConfig.taskScanInterval);
			}
		} catch (Exception e) {
			logger.error(e.getMessage(), e);
		}
	}
}
