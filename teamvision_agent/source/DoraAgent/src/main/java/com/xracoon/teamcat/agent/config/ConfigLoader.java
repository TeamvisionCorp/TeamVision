package com.xracoon.teamcat.agent.config;

import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.Properties;
import org.apache.log4j.Logger;

/**
 * Agent配置加载器
 * @author Yangtianxin
 */
public class ConfigLoader {
	Logger logger = Logger.getLogger(ConfigLoader.class);
	
	public AgentConfig load(String path)
	{
		//new with default value
		AgentConfig config=new AgentConfig();
		
		try
		{
//			//load global value
//			logger.info("load global config settings from database...");
//			
//			DicdataService dataServer=new DicdataService();
//			Map<String,Object> map=dataServer.getAgentGlobalConfig();
//			if(map.containsKey("DevScanInterval"))
//				config.devScanInterval=(Integer)map.get("DevScanInterval");
//			if(map.containsKey("TaskScanInterval"))
//				config.taskScanInterval=(Integer)map.get("TaskScanInterval");	
//			if(map.containsKey("AgentDefaultPort"))
//				config.agentPort=(Integer)map.get("AgentDefaultPort");	
//			if(map.containsKey("AgentDefaultSpace"))
//				config.workDir=(String)map.get("AgentDefaultSpace");	
//			if(map.containsKey("GitUser"))
//				config.gitAccount=(String)map.get("GitUser");	
//			if(map.containsKey("GitPassword"))
//				config.gitPasswd=(String)map.get("GitPassword");	
//			if(map.containsKey("SvnUser"))
//				config.svnAccount=(String)map.get("SvnUser");	
//			if(map.containsKey("SvnPassword"))
//				config.svnPasswd=(String)map.get("SvnPassword");	
//			if(map.containsKey("WifiConnectTimeout"))
//				config.WifiConnectTimeout=(Integer) map.get("WifiConnectTimeout");	
//			
//			if(map.containsKey("FtpServer"))
//				config.FtpServer=(String)map.get("FtpServer");	
//			if(map.containsKey("FtpPort"))
//				config.FtpPort=(Integer)map.get("FtpPort");
//			if(map.containsKey("FtpUser"))
//				config.FtpUser=(String)map.get("FtpUser");
//			if(map.containsKey("FtpPasswd"))
//				config.FtpPasswd=(String)map.get("FtpPasswd");
//			if(map.containsKey("FtpRootDir"))
//				config.FtpArchiveRoot=(String)map.get("FtpRootDir");
//			if(map.containsKey("rerunTimeDefualt"))
//				config.rerunTime=(Integer)map.get("rerunTimeDefualt");
//			if(map.containsKey("rerunIsUpdateResult"))
//				config.rerunIsUpdateResult=((Integer)map.get("rerunIsUpdateResult")>0);
			
			
			//load local value
			File file=new File(path);
			if(file.exists())
			{
				logger.info("loading local config settings from '"+path+"'...");
				
				Properties agentProp=new Properties();
		    	InputStream pFileStream=new FileInputStream(path);
		    	agentProp.load(pFileStream);
		    	pFileStream.close();
		    	
//		    	if(agentProp.containsKey("scm.git.account"))
//		    		config.gitAccount=agentProp.getProperty("scm.git.account");
//		    	if(agentProp.containsKey("scm.git.passwd"))
//		    		config.gitPasswd=agentProp.getProperty("scm.git.passwd");
//		    	if(agentProp.containsKey("scm.svn.account"))
//		    		config.svnAccount=agentProp.getProperty("scm.svn.account");
//		    	if(agentProp.containsKey("scm.svn.passwd"))
//		    		config.svnPasswd=agentProp.getProperty("scm.svn.passwd");
		    	
		    	if(agentProp.containsKey("agent.debug.archive"))
		    		config.debugArchive=Boolean.parseBoolean(agentProp.getProperty("agent.debug.archive"));
		    	if(agentProp.containsKey("agent.debug.codefetch"))
		    		config.debugCodefetch=Boolean.parseBoolean(agentProp.getProperty("agent.debug.codefetch"));
		    	if(agentProp.containsKey("agent.forceclean"))
		    		config.forceClean=Boolean.parseBoolean(agentProp.getProperty("agent.forceclean"));
		    	if(agentProp.containsKey("agent.debug.caseshrink"))
		    		config.debugCaseShrink=Integer.parseInt(agentProp.getProperty("agent.debug.caseshrink"));
		    	if(agentProp.containsKey("agent.alivecheck.timeout"))
		    		config.aliveCheckInterval=1000*Integer.parseInt(agentProp.getProperty("agent.alivecheck.timeout"));
		    	if(agentProp.containsKey("agent.logcache.batch"))
		    		config.logCacheBatch=Integer.parseInt(agentProp.getProperty("agent.logcache.batch"));
		    	if(agentProp.containsKey("agent.logcache.timeoutsec"))
		    		config.logCacheTimeoutSec=1000*Integer.parseInt(agentProp.getProperty("agent.logcache.timeoutsec"));
			}
			else
			{
				logger.info("can't find local config file '"+path+"',  skip loading local settings");
			}
	    	
		}catch(Exception e)
		{
			logger.error(e.getMessage(), e);
		}

		return config;
	}
}
