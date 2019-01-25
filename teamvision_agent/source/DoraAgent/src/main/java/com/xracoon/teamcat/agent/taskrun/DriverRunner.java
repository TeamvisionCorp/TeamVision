package com.xracoon.teamcat.agent.taskrun;

import java.io.File;
import java.io.IOException;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;

import com.xracoon.teamcat.agent.webservice.AgentWebService;
import com.xracoon.teamcat.driver.*;
import com.xracoon.util.basekit.StringEx;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.xracoon.teamcat.agent.config.AgentConfig;
import com.xracoon.teamcat.agent.file.AntFileUtil;
import com.xracoon.teamcat.driver.DriverLauncher.LaunchParams;
import com.xracoon.teamcat.driver.args.DriverArg;
import com.xracoon.util.basekit.hudson.proc.NullStream;
import com.xracoon.util.basekit.hudson.proc.Proc;
import com.xracoon.util.basekit.system.OS;

public class DriverRunner {
	public Logger logger = LoggerFactory.getLogger(DriverRunner.class);
	public Proc proc;
	
	private AgentConfig config;
	private OS os;
	private TaskInfo info;
	private Map<String,String> hostMap;
	private WorkdirManager dirManager;
	private ArchiveManager archiveManager;

	private volatile String error;
	private String hostbackFile="./hosts.bak";
	private List<Integer[]> statics=new ArrayList<Integer[]>();
	
	public boolean isAlive() throws IOException, InterruptedException{
		return proc!=null && proc.isAlive();
	}
	
	public Boolean getResult() throws IOException, InterruptedException{
		if(proc==null || proc.isAlive())
			return null;
		else
			return proc.join()==0;
	}
	
	public String getErrorMsg() {
		return error;
	}
	public void setRunError(String error){
		this.error=error;
	}

	@SuppressWarnings("unchecked")
	public DriverRunner(AgentConfig config, OS os, TaskInfo info) {	
		this.os=os.clone();
		this.config = config;
		this.info=info;
		
		if(info.options!=null && info.options.size()>0){
			if(info.options.containsKey(DriverArg.HOSTMAP));
				this.hostMap=(Map<String, String>) info.options.get(DriverArg.HOSTMAP);
		}
		
		this.dirManager=new WorkdirManager(config.workDir);
		dirManager.setLogger(logger);
		
		archiveManager=new WebApiArchiveManager(info);
		//archiveManager=new FtpArchiveManager(info, config.FtpServer, config.FtpPort, config.FtpUser, config.FtpPasswd,  config.FtpArchiveRoot);
		archiveManager.setLogger(logger);
	}
	
	public void printTaskResultSummary()
	{
		logger.info("-----------------------------------------------");
		logger.info("\t task result summay");
		logger.info("-----------------------------------------------");
		logger.info("statics of "+statics.size()+" batchs: ");
		if(statics.size()>0)
		{
			int i=0;
			int allRunNum=0;
			for(Integer[] ia: statics)
			{
				logger.info("\t batch "+(++i)+":   num="+ia[0]+",  unpassed="+ia[1]+",   passed="+(ia[0]-ia[1]));
				allRunNum+=ia[0];
			}
			logger.info("statics summary: ");
			logger.info("\t runNum="+allRunNum+",  runBatchNum="+statics.size());
			int caseNum=statics.get(0)[0];
			int stillUnpassed=statics.get(statics.size()-1)[1];
			logger.info("\t caseNum="+statics.get(0)[0]+",  stillUnpassed="+stillUnpassed+",   allPassed="+(caseNum-stillUnpassed));
		}
		logger.info("-----------------------------------------------");
	}
	
	public void postWork(String codePath, AgentNotifierImpl notifier){
		logger.info("===>execute task done:"+info.taskQueueID);
		printTaskResultSummary();
		if(!OS.isMac() && hostMap!=null && hostMap.size()>0 && info.taskType!=DatasEnum.AutoTaskType_APPUI.getValue()){
			try {
				logger.info("resotre host...");
				os.resotreHost(hostbackFile);
			} catch (IOException e1) {
				logger.error("resotre host error: "+ e1.getMessage(),e1);
			}
		}
		if(codePath!=null  && config.debugArchive/*&& (forceStop==null || !forceStop)*/)
		{
			try {
				//notifier.requestArchiveAll(codePath);
				//notifier.archiveLogFile(getLogFile(info));
			} catch (Exception e1) {
				logger.error("archive error: "+ e1.getMessage(),e1);
			}
		}
	}
	
	public void runProcess() throws Exception{
		//boolean cleanWorkspace=true;
		//logger.info("===>prepare workspace, clean: "+cleanWorkspace);
		//dirManager.prepare(info, cleanWorkspace);  //环境创建放到Driver中
		
		logger.info("===>run task process : t"+info.taskID+"_tq"+info.taskQueueID);
		
		//查找DoraDriver*.jar
		//taskId, taskType, tqId, historyID, paramId, agnetId, workspace, agentPort, toolpath
		OutputStream nos=new NullStream();
		File[] files=AntFileUtil.listAllFull(new File(config.agentHome, "libs"), "teamcat-driver*.jar", null);
		LaunchParams lparam=new LaunchParams(info, config.agentPort, dirManager.getTaskDir(info).getCanonicalPath() ,config.buillToolsPath);
		String pa=lparam.toJson().toString();
		proc=new Proc.LocalProc(new String[]
				{ "java","-jar", files[0].getAbsolutePath(), lparam.toJson().replace("\"", "'")},
				null, System.in, nos, nos, new File("."), logger, true);
		Long timeOut = AgentWebService.getAgentTimeOutMileSec();
		if(timeOut!=null){
			proc.joinWithTimeout(timeOut, TimeUnit.MILLISECONDS,logger);
		}else{
			proc.joinWithTimeout(7200000, TimeUnit.MILLISECONDS,logger);
		}

	}
	
	public void stop() throws IOException, InterruptedException{
		if(proc!=null)
			proc.kill();
	}
}
