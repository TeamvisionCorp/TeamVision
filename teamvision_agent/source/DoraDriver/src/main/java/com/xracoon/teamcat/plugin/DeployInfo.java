package com.xracoon.teamcat.plugin;

import java.io.Serializable;
import java.util.Date;
import java.util.List;
import java.util.Map;

import net.sf.json.JSONObject;

public class DeployInfo implements Serializable {
	private static final long serialVersionUID = 5321145444420639701L;
	
	private long id;
	private Date CreateTime;
	private boolean IsActive;
	private String ServieName;
	private String DeployDir;
	private String AccessLog;
	private String ErrorLog;
	private String StartCommand;
	private String StopCommand;
	private String RestartCommand;
	private List<String> RelatedFiles;
	private List<String> DeployScripts;
	private Map<String, String> AdvanceConfig;
	private long Project;
	
	public static DeployInfo fromJson(JSONObject json){
		DeployInfo di=new DeployInfo();
		di.setId(json.getInt("id"));
		//di.setCreateTime(json.get);
		//di.setIsActive(json.getBoolean("IsActive"));
		di.setServieName(json.getString("ServiceName"));
		di.setDeployDir(json.getString("DeployDir"));
		di.setAccessLog(json.getString("AccessLog"));
		di.setErrorLog(json.getString("ErrorLog"));
		di.setStartCommand(json.getString("StartCommand"));
		di.setStopCommand(json.getString("StopCommand"));
		di.setRestartCommand(json.getString("RestartCommand"));
		//di.setRelatedFiles(relatedFiles);
		//di.setDeployScripts();
		//di.setAdvanceConfig(advanceConfig);
		di.setProject(json.getInt("Project"));
		
		return di;
	}
	public long getId() {
		return id;
	}
	public void setId(long id) {
		this.id = id;
	}
	public Date getCreateTime() {
		return CreateTime;
	}
	public void setCreateTime(Date createTime) {
		CreateTime = createTime;
	}
	public boolean isIsActive() {
		return IsActive;
	}
	public void setIsActive(boolean isActive) {
		IsActive = isActive;
	}
	public String getServieName() {
		return ServieName;
	}
	public void setServieName(String servieName) {
		ServieName = servieName;
	}
	public String getDeployDir() {
		return DeployDir;
	}
	public void setDeployDir(String deployDir) {
		DeployDir = deployDir;
	}
	public String getAccessLog() {
		return AccessLog;
	}
	public void setAccessLog(String accessLog) {
		AccessLog = accessLog;
	}
	public String getErrorLog() {
		return ErrorLog;
	}
	public void setErrorLog(String errorLog) {
		ErrorLog = errorLog;
	}
	public String getStartCommand() {
		return StartCommand;
	}
	public void setStartCommand(String startCommand) {
		StartCommand = startCommand;
	}
	public String getStopCommand() {
		return StopCommand;
	}
	public void setStopCommand(String stopCommand) {
		StopCommand = stopCommand;
	}
	public String getRestartCommand() {
		return RestartCommand;
	}
	public void setRestartCommand(String restartCommand) {
		RestartCommand = restartCommand;
	}
	public List<String> getRelatedFiles() {
		return RelatedFiles;
	}
	public void setRelatedFiles(List<String> relatedFiles) {
		RelatedFiles = relatedFiles;
	}
	public List<String> getDeployScripts() {
		return DeployScripts;
	}
	public void setDeployScripts(List<String> deployScripts) {
		DeployScripts = deployScripts;
	}
	public Map<String, String> getAdvanceConfig() {
		return AdvanceConfig;
	}
	public void setAdvanceConfig(Map<String, String> advanceConfig) {
		AdvanceConfig = advanceConfig;
	}
	public long getProject() {
		return Project;
	}
	public void setProject(long project) {
		Project = project;
	}
}
