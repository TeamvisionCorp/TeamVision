package com.xracoon.teamcat.driver;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;

import com.xracoon.teamcat.agent.device.Device;
import com.xracoon.teamcat.plugin.TaskConfig;

/**
 * 任务信息结构
 * @author Yangtianxin
 */
public class TaskInfo implements Serializable {
	private static final long serialVersionUID = 1843261642694269975L;
	
	public long taskID;
	public int taskType;
	public long taskQueueID;
	public long historyID;
	public String testTaskResultID;
	public int agentID;
	public String paramID;
	
	public TaskConfig taskConfig;
	public Map<String,Object> options=new HashMap<>();
	
	@Deprecated public String runUUID;
	
	//public Map<String,String> hosts;
	public String deviceSNo;
	public Integer deviceId;
	public Device device;
}
