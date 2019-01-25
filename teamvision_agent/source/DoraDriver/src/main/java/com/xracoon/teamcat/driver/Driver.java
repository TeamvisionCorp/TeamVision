package com.xracoon.teamcat.driver;

import java.util.HashMap;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.xracoon.teamcat.agent.device.Device;
import com.xracoon.teamcat.plugin.TaskConfig;
import com.xracoon.util.basekit.system.OS;

public abstract class Driver {
	public static final int ARCHIVE_PACKAGE=1;
	public static final int ARCHIVE_LOG=2;
	public static final int ARCHIVE_ZIPALL=3;

	public static final String TEST_CASE_TYPE_INTERFACE="1";//接口case
	public static final String TEST_CASE_TYPE_WEBUI="2";//webUI
	
	public static final String ENV_WORKSPACE="ENV_WORKSPACE";
	public static final String ENV_NOTIFIER="ENV_NOTIFIER";
	public static final String ENV_LASTVERSION="ENV_LASTVERSION";
	public static final String ENV_CHANGESET="ENV_CHANGESET";
	public static final String ENV_PACKAGEINFO="ENV_PACKAGEINFO";
	public static final String ENV_VERSIONMAP="ENV_VERSIONMAP";
	public static final String ENV_BUILDTOOLS="ENV_BUILDTOOLS";
	public static final String ENV_TASKCONFIG="ENV_TASKCONFIG";
	public static final String ENV_TOKENS="ENV_TOKENS";
	public static final String ENV_HISTORYID="ENV_HISTORYID";
	public static final String ENV_TESTRESULTID="ENV_TESTRESULTID";
	public static final String ENV_SCMSTEPIDX="ENV_SCMSTEPIDX"; //向SCM插件提供它的序号信息
	
	public static final String TOK_WORKSPACE="WORKSPACE";
	public static final String TOK_DEPLOYSPACE="DEPLOYSPACE";
	public static final String TOK_DEPLOYPATH="DEPLOYPATH";
	public static final String TOK_PARAMGROUP="PARAMETERGROUPNAME";
	public static final String TOK_SCMVERSION="SCM_VERSION";
	public static final String TOK_LASTVERSION="LASTVERSION";
	public static final String TOK_BUILDVERSION="BUILDVERSION";
	public static final String TOK_TASKID="TASKID";
	public static final String TOK_BUILDTOOL="BUILDTOOL";
	public static final String TOK_COMMONSPACE="COMMONSPACE";
	public static final String TOK_TASKNAME="TASKNAME";
	public static final String TOK_BUILDBACKUPSPACE="BUILDBACKUPSPACE";
	public static final String TOK_HISTORYID="HISTORYID";

	
	
	protected Logger logger=LoggerFactory.getLogger(Driver.class);
	protected String workspace;
	private TaskConfig taskConfig;
	
	private AgentNotifier notifier;
	protected Map<String,Object> env;
	protected Map<Integer,CaseAssign> caseMap;
	private volatile String resultMessage;
	private OS os;
	private Device device;

	@SuppressWarnings("unchecked")
	public Map<String,String> getTokens(){
		return (Map<String, String>) env.get(ENV_TOKENS);
	}
	
	protected boolean isInit;
	public final boolean isInitialized(){
		return isInit;
	}
	public final OS getOs() {
		return os;
	}
	public final void setOs(OS os) {
		this.os = os;
	}
	public final Device getDevice() {
		return device;
	}
	public final void setDevice(Device device) {
		this.device = device;
	}
	public final void setLogger(Logger logger){
		this.logger=logger;
	}
	public final void setMessage(String msg){
			resultMessage=msg;
	}
	public final String getMessage(){
		return resultMessage;
	}
	public final AgentNotifier getNotifier(){
		return this.notifier;
	}
	public final void setNotifier(AgentNotifier notifier){
		this.notifier=notifier;
	}
	
	public final void setEnvs(Map<String,Object> env){
		this.env=env;
	}
	public final void setCaseMap(Map<Integer,CaseAssign> list){
		this.caseMap=list;
	}
	public final Map<Integer,CaseAssign> getCaseMap(){
		return this.caseMap;
	}
	
	public final void setTaskConfig(TaskConfig taskConfig){
		this.taskConfig=taskConfig;
	}
	public final TaskConfig getTaskConfig(){
		return this.taskConfig;
	}
	public String getWorkspace() {
		return workspace;
	}
	public void setWorkspace(String workspace) {
		this.workspace = workspace;
	}
	
	protected final Map<String,String> getDriverArgs(String driverArgs)
	{
		Map<String,String> args=new HashMap<String,String>();
		if(driverArgs!=null)
		{
			String[] lines=driverArgs.split("\n|;|&");//
			for(String line: lines)
			{
				if(line.trim().length()>0 && line.contains("="))
				{
					String[] parts=line.split("=",2);
					args.put(parts[0].trim(),parts[1].trim());
				}
			}
		}
		return args;
	}
	
	public abstract String[] getArgsDesc();
	
	/**
	 * main work of drivers should be implement in this method. This method may be call many times. 
	 * @return 
	 */
	public abstract boolean exec();
	/**
	 * one time prepare work should be implement in this method.
	 * @return
	 */
	public abstract boolean init();
	public abstract boolean stop();
}
