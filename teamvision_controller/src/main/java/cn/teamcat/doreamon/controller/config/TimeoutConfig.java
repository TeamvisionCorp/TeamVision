package cn.teamcat.doreamon.controller.config;

import java.util.List;

import org.apache.ibatis.session.SqlSession;

import cn.teamcat.doreamon.controller.tools.Constants;
import cn.teamcat.doreamon.controller.tools.HttpClientHelperBasic;
import cn.teamcat.doreamon.controller.tools.SessionFactoryUtil;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

public class TimeoutConfig {
	
	public Integer taskWaitTimeout; 
	public Integer TaskRunTimeout;
	public Integer LockTimeout;
	public Integer SocketTimeout;
	
	public TimeoutConfig(){
		try {
			Integer EmailConfigtypeid = 16;
			JSONObject EmailConfigRsp = HttpClientHelperBasic.get(Constants.API.GET_DICCONFIG+EmailConfigtypeid+"/dicconfigs", null);
		    JSONArray result = EmailConfigRsp.getJSONArray("result");			
		for (int i = 0; i < result.size(); i++) {
			JSONObject data = result.getJSONObject(i);
			String dataName = data.getString("DicDataName");
			Integer dataValue = data.getInt("DicDataValue");
			if (dataName.equals("TaskWaitTimeout")) {
				setTaskWaitTimeout(dataValue);
				continue;
			}
			if (dataName.equals("TaskRunTimeout")) {
				setTaskRunTimeout(dataValue);
				continue;
			}
			if (dataName.equals("LockTimeout")) {
				setLockTimeout(dataValue);
				continue;
			}
			if (dataName.equals("SocketTimeout")) {
				setSocketTimeout(dataValue);
				continue;
			}
		}
		} catch (Exception e) {
			// TODO: handle exception
		}
	}
	
	public Integer getTaskWaitTimeout() {
		return taskWaitTimeout;
	}
	public void setTaskWaitTimeout(Integer taskWaitTimeout) {
		this.taskWaitTimeout = taskWaitTimeout;
	}
	public Integer getTaskRunTimeout() {
		return TaskRunTimeout;
	}
	public void setTaskRunTimeout(Integer taskRunTimeout) {
		TaskRunTimeout = taskRunTimeout;
	}
	public Integer getLockTimeout() {
		return LockTimeout;
	}
	public void setLockTimeout(Integer lockTimeout) {
		LockTimeout = lockTimeout;
	}
	public Integer getSocketTimeout() {
		return SocketTimeout;
	}
	public void setSocketTimeout(Integer socketTimeout) {
		SocketTimeout = socketTimeout;
	}
}
