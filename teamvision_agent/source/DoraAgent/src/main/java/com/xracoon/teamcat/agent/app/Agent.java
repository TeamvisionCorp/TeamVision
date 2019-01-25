package com.xracoon.teamcat.agent.app;

import java.io.IOException;

import com.xracoon.teamcat.agent.utils.RedisUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.xracoon.teamcat.agent.config.AgentConfig;
import com.xracoon.teamcat.agent.device.DeviceMonitor;
import com.xracoon.teamcat.agent.network.CmdMsg;
import com.xracoon.teamcat.agent.network.INetCmdListener;
import com.xracoon.teamcat.agent.network.NetCmd;
import com.xracoon.teamcat.agent.network.NetServer;
import com.xracoon.teamcat.agent.network.ReAliveChecker;
import com.xracoon.teamcat.agent.network.StatusUpdater;
import com.xracoon.teamcat.agent.taskrun.TaskExecutor;
import com.xracoon.teamcat.agent.webservice.AgentWebService;
import com.xracoon.teamcat.driver.DatasEnum;
import com.xracoon.teamcat.driver.TaskInfo;
import com.xracoon.util.basekit.StringEx;
import com.xracoon.util.basekit.system.OS;

/**
 * Agent主控制器,启动和调度各个工作线程
 * @author Yangtianxin
 */
public class Agent extends ThreadGroup  implements INetCmdListener, StatusUpdater{
	private Logger logger=LoggerFactory.getLogger(Agent.class);
	
	private TaskExecutor executor;
	private AgentConfig config;
	private NetServer netMonitor;
	private DeviceMonitor deviceMonitor;
	private OS os;
	
	public Agent(AgentConfig conf) throws Exception
	{
		super("AgentThreadGroup");
		this.config=conf;
		init();
	}
	
	public DeviceMonitor getDeviceMonitor(){
		return deviceMonitor;
	}

	
	private void init() throws Exception {
		logger.info("Agent init....");
		os=OS.getNewInstance();
		os.setLogger(logger);
		logger.info("Current OS: "+os.getOs()+"_"+os.getArch()+"_"+os.getVersion()+", "+os.getDomain()+"/"+os.getName()+", ip:"+os.getIP(null));
		
		//backup host and check running role
		if(!ConsoleLauncher.isDebug){
			try{
				if(!OS.isMac())
					os.backupHost(os.getHostPath()+".dorabak");
			}catch(IOException e){
				throw new Exception("无权限访问host文件", e);
			}
		}
		////更新Agent状态, 改为启动时从命令行参数读取
		//config.agentKey = os.getIP(null);	
		
		logger.info("Agent Key: "+config.agentKey);
		AgentWebService.agentInfo(config);
	};
	
	public void upateStatus(){
		try {
			if(AgentWebService.agentUpate(config.agentKey, DatasEnum.AutoAgentStatus_Online.getValue())!=0){
				logger.warn("!! Status update failed. Updating will be try again later.");
			}
			else
				logger.warn("Agent Status Updated: "+config.agentId+"   "+config.agentKey+":"+config.agentPort+"  online");
		} catch (Exception e) {
			logger.warn("!! Status update failed. Updating will be try again later.",e);
		}
	}
	
	public void start() throws Exception{
		logger.info("start work thread...");
		startNetMonitor();
		//startDeviceMoniter();	
		startTaskExecutor();
		
		if(AgentWebService.agentUpate(config.agentKey, DatasEnum.AutoAgentStatus_Online.getValue())!=0)
			throw new Exception("Agent状态同步失败!");
		
		logger.info("Agent Status Updated: "+config.agentId+"   "+config.agentKey+":"+config.agentPort+"  online");
		logger.info("Agent start done");
		
		//startAliveChecker();
	};
	
	private void startTaskExecutor() {
		executor=new TaskExecutor(this);
		executor.setDaemon(true);
		executor.start();
	}
	private void startAliveChecker(){
		Thread aliveCheckThread= new Thread(new ReAliveChecker(this, config.aliveCheckInterval));
		aliveCheckThread.setDaemon(true);
		aliveCheckThread.start();
	}

	private void startNetMonitor(){
		netMonitor=new NetServer(this, RedisUtils.jedisPool);
		netMonitor.start();
		//new Thread(this,netMonitor).start();
	}
	
//	private void startDeviceMoniter(){
//		deviceMonitor=new DeviceMonitor(this);
//		deviceMonitor.setDaemon(true);
//		deviceMonitor.start();
//	}
	
	public  TaskInfo ToTaskInfo(NetCmd cmd){
		TaskInfo info=new TaskInfo();
		info.taskID=Long.parseLong(cmd.args.get("taskId"));
		info.taskType=Integer.parseInt(cmd.args.get("taskType"));
		info.taskQueueID= cmd.tqID;
		info.agentID=config.agentId;
		info.historyID=Long.parseLong(cmd.args.get("historyId"));
		info.paramID=StringEx.isBlank(cmd.args.get("parameterId"))?null:(cmd.args.get("parameterId"));
		
		info.testTaskResultID= cmd.args.get("testTaskResult");
		
		return info;
	}
	public String startTask(NetCmd cmd){	
		//当前无任务，启动任务线程
		logger.info("Start Task: "+cmd.tqID);
		String error=executor.addTask(ToTaskInfo(cmd));
		if(error!=null)
			logger.info(error);

		return error;
	}

	public String stopTask(NetCmd cmd) {
		logger.info("process stop task:  "+cmd.type+","+cmd.tqID);
		String error=executor.stopTask(cmd.tqID,  cmd.type==CmdMsg.Timeout);
		if(error!=null)
			logger.error(error);
		return error;
	}

	public boolean aliveTest(NetCmd cmd) {
		logger.info("process alive test");
		return true;
	}
	public boolean stopAgent(NetCmd cmd) {
		shutdown();
		return true;
	}
	public String queryTaskState(NetCmd cmd) {
		return executor.queryTaskState();
	}
	@Override
	public void runError(NetCmd cmd) {
		executor.setDriverError(Long.parseLong(cmd.args.get("tqId")), cmd.args.get("msg"));
	}
	
	@Override
	 public void uncaughtException(Thread t, Throwable e){   
		if(e instanceof ThreadDeath){
			logger.error("Thread death: "+t.getName());
			return ;
		}
		logger.error("Exception in Thread: "+t.getName());
		logger.error(e.getMessage(), e);
		shutdown();
     } 
	 
	public void shutdown() {
		logger.info("agent shutdown...");
		System.exit(-1);
	}
	
	
	public AgentConfig getAgentConfig()
	{
		return config;
	}
	public OS getOS()
	{
		return os;
	}
}
