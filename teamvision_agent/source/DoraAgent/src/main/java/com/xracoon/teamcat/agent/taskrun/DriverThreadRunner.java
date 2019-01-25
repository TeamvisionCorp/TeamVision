package com.xracoon.teamcat.agent.taskrun;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.xracoon.teamcat.agent.config.AgentConfig;
import com.xracoon.teamcat.driver.ArchiveManager;
import com.xracoon.teamcat.driver.CaseAssign;
import com.xracoon.teamcat.driver.DatasEnum;
import com.xracoon.teamcat.driver.Driver;
import com.xracoon.teamcat.driver.DriverLoader;
import com.xracoon.teamcat.driver.TaskInfo;
import com.xracoon.teamcat.driver.WebApiArchiveManager;
import com.xracoon.teamcat.driver.WebService;
import com.xracoon.teamcat.driver.args.DriverArg;
import com.xracoon.util.basekit.system.OS;

public class DriverThreadRunner  extends Thread {
	public Logger logger = LoggerFactory.getLogger(DriverThreadRunner.class);
	
	private AgentConfig config;
	private OS os;
	private TaskInfo info;
	private Map<String,String> hostMap;
	private ArchiveManager archiveManager;
	private Driver driver;
	private volatile Boolean result;
	private volatile String message;
	private volatile Boolean forceStop;
	private String hostbackFile="./hosts.bak";
	private List<Integer[]> statics=new ArrayList<Integer[]>();
	
	public Boolean getResult() {
		return result;
	}

	public String getMessage() {
		return message;
	}
	
	public Boolean isForceStop() {
		return forceStop;
	}

	@SuppressWarnings("unchecked")
	public DriverThreadRunner(AgentConfig config, OS os, TaskInfo info) {
		super("DriverRunnerThread_TQ"+info.taskQueueID);
		
		this.os=os.clone();
		this.config = config;
		this.info=info;
		
		if(info.options!=null && info.options.size()>0){
			if(info.options.containsKey(DriverArg.HOSTMAP));
				this.hostMap=(Map<String, String>) info.options.get(DriverArg.HOSTMAP);
		}
		
		archiveManager=new WebApiArchiveManager(info);
		//archiveManager=new FtpArchiveManager(info, config.FtpServer, config.FtpPort, config.FtpUser, config.FtpPasswd,  config.FtpArchiveRoot);
		archiveManager.setLogger(logger);
	}

	public Driver getDriver() {
		return this.driver;
	}
	
	public void forceStop()
	{
		logger.info("------DriverRunner forceStop------");
		if(driver!=null)
			driver.stop();
		forceStop=true;
		result=false;
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
		
		if(forceStop==null)
			forceStop=false;
	}
	
	@Override
	public void run() {
		String codePath=null;
		AgentNotifierImpl notifier=null;
		os.setLogger(logger);
		boolean ret=false;
		
		logger.info("===>run task : t"+info.taskID+"_tq"+info.taskQueueID);
		try{
			logger.info("---------------------------------------------");
			logger.info("\t task detail");
			logger.info("---------------------------------------------");
			logger.info("taskId:\t"+info.taskID);
			logger.info("taskName:\t"+info.taskConfig.getTaskName());
			logger.info("taskQueueId:\t"+info.taskQueueID);
			logger.info("taskType:\t"+info.taskType);
			
			Map<Integer,CaseAssign> caseMap=null;
			if(info.options!=null && info.options.containsKey(DriverArg.CASELIST)){
				@SuppressWarnings("unchecked")
				Map<Integer,String> caseMapRaw=(Map<Integer,String>)info.options.remove(DriverArg.CASELIST);
				caseMap=new HashMap<Integer,CaseAssign>();
				StringBuilder cases=new StringBuilder();
				if(caseMapRaw==null)
					throw new Exception("case list is empty");
	
				int cnum=0;
				for(Entry<Integer,String> entry:caseMapRaw.entrySet())
				{
					cases.append(entry.getKey()+" ");
					caseMap.put(entry.getKey(), new CaseAssign(entry.getKey(),entry.getValue()));
					if((++cnum)==config.debugCaseShrink)    //must be euqal
						break;
				}
				
				logger.info("caseNumber:\t"+caseMapRaw.size());
				if(config.debugCaseShrink>0)
					logger.info("caseShrinksTo:\t"+config.debugCaseShrink);
				logger.info("caseDetail:\t"+cases);
				logger.info("maxRerun:\t"+config.rerunTime);
				logger.info("rerunIsUpdateResult:\t"+config.rerunIsUpdateResult);
				if(info.device!=null)
					logger.info("useDevice:\t"+info.device);
			}
			
			logger.info("driverOptions:\t"+info.options.get(DriverArg.DRIVERARG));
			logger.info("---------------------------------------------");
//			dirManager.prepare(info,true);  //准备环境
			
//			codePath=dirManager.getTaskDir(info).getAbsolutePath();
//			info.options.put(DriverArg.WORKSPACE, codePath);
			
			//trimCase(info);
			
			//源码(与本机器相关)
//			if(config.debugCodefetch && (info.taskType==DatasEnum.AutoTaskType_APPUI.getValue()
//					|| info.taskType==DatasEnum.AutoTaskType_Interface.getValue()) )
//				pullSouceCode(info.codeURL, info.codeVersion, info.account, info.pwdOrPrikey, codePath);
				
			//环境配置
			if(!OS.isMac() && hostMap!=null && hostMap.size()>0 && info.taskType!=DatasEnum.AutoTaskType_APPUI.getValue()){
				logger.info("backup host...");
				os.backupHost(hostbackFile);
				os.updateHost(hostMap);
			}
			
			//调用Driver
			String driverClassName="";
			if(info.taskType==DatasEnum.AutoTaskType_APPUI.getValue())
				driverClassName="com.xracoon.teamcat.driver.aui.AndroidUITestDriver";
			else if(info.taskType==DatasEnum.AutoTaskType_Interface.getValue())
				driverClassName="com.xracoon.teamcat.driver.interfacetest.InterfaceDriver";
			else if(info.taskType==DatasEnum.AutoTaskType_PACKAGE.getValue())
				driverClassName="com.xracoon.teamcat.driver.pack.PackageDriver";
			else if(info.taskType==DatasEnum.AutoTaskType_DEPLOY.getValue())
				driverClassName="com.xracoon.teamcat.driver.deploy.DeployDriver";
			else
				throw new Exception("unhandlable taskType: "+info.taskType);
							
			DriverLoader driverLoader=new DriverLoader(".");
			driverLoader.setLogger(logger);
			driver=driverLoader.loadDriver(driverClassName);
			driver.setLogger(logger);
			driver.setOs(os);
			notifier=new AgentNotifierImpl(info,archiveManager, config.rerunIsUpdateResult);
			notifier.setLogger(logger);
			
			if(info.taskType==DatasEnum.AutoTaskType_APPUI.getValue() || info.taskType==DatasEnum.AutoTaskType_Interface.getValue())
				notifier.resetCaseAssignList(caseMap);
			
			driver.setNotifier(notifier);
			driver.setEnvs(info.options);
			driver.setDevice(info.device);
			driver.setTaskConfig(info.taskConfig);
			info.options.put(DriverArg.WIFITIMEOUT, config.WifiConnectTimeout);
			
			
			//查询lastVersion
			try{
				info.options.put(Driver.ENV_LASTVERSION, WebService.getLastVersion(info.taskID));
			}catch(Exception e0){
				logger.error("exception when query last version", e0);
			}
			
			logger.info("Driver for task t"+info.taskID+"("+info.taskConfig.getTaskName()+")_tq"+info.taskQueueID+" is running ...");
			if(!driver.init())
				throw new Exception("driver initialize failed");

			//执行非测试任务
			if(info.taskType!=DatasEnum.AutoTaskType_APPUI.getValue() && info.taskType!=DatasEnum.AutoTaskType_Interface.getValue()){
				ret=driver.exec();	
				if(driver.getMessage()!=null&&driver.getMessage().trim().length()>0)
					message=ret+" "+(message==null?"":message)+": "+driver.getMessage();
			}
			//执行测试任务
			else{
				Map<Integer,CaseAssign> unpassed=notifier.getNotPassedCases();
				int runbatch=Math.max(1, config.rerunTime+1);
				for(int i=1; i<=runbatch && unpassed.size()>0; i++)
				{
					int totalCaseNum=unpassed.size();
	
					logger.info("");
					logger.info("-------------------"+"Run batch "+i+"/"+runbatch+(i>1?" (rerun)":"")+"    unpassed case num: "+totalCaseNum+"------------------");
					
					driver.setCaseMap(unpassed);
					boolean iret=driver.exec();	
					if(driver.getMessage()!=null&&driver.getMessage().trim().length()>0)
						message=(message==null?"":message)+(i>1?"\n Run batch "+i+" : ":"")+driver.getMessage();
					
					notifier.printResultSummary();
					unpassed=notifier.getNotPassedCases();
					statics.add(new Integer[]{totalCaseNum, unpassed.size()});
					
					if(i==1)
					{
						ret=iret;
						if(!ret)
							break;
					}		
				}
			}

			try {
				postWork(codePath, notifier);
				result=ret;
			} catch (Exception e0) {
				logger.error(e0.getMessage(), e0);
			}
		}
		catch(Exception e)
		{
			//任务执行失败
			ret=false;
			message="Exception in DriverRunner : "+e.getMessage();
			if(driver!=null && driver.getMessage()!=null)
				message+="\nDriver: "+driver.getMessage();
			
			logger.error(e.getMessage(), e);
			postWork(codePath, notifier);
			result=ret;
		}
	}
}
