package com.xracoon.teamcat.agent.config;

/**
 * Agent配置结构体
 * @author Yangtianxin
 */
public class AgentConfig {
	public String agentKey;
	public String agentName;
	//public String agentIP;
	public int agentId;
	public int agentPort=8099;
	public String workDir="./workspace";
	public String agentHome=".";
	public String buillToolsPath;
	
	public int devScanInterval=5000;
	public int taskScanInterval=3000;
	public int WifiConnectTimeout=60000;
	public int aliveCheckInterval=60000+1;
	public int logCacheBatch=500;
	public int logCacheTimeoutSec=5;
//	public String gitAccount="autotest";
//	public String gitPasswd="Nopass.2";
//	public String svnAccount="autotest";
//	public String svnPasswd="Nopass.2";
//	
	public String FtpServer="10.2.44.58";
	public int FtpPort=21;
	public String FtpUser="root";
	public String FtpPasswd="root";
	public String FtpArchiveRoot="archives";
	
	public boolean debugArchive=true;
	public boolean debugCodefetch=true;
	public boolean forceClean=false;
	
	
	public int rerunTime=0;
	public boolean rerunIsUpdateResult=false;
	public int debugCaseShrink=0;
}
