package cn.teamcat.doreamon.controller.config;

import java.util.List;

import org.apache.ibatis.session.SqlSession;

import cn.teamcat.doreamon.controller.tools.Constants;
import cn.teamcat.doreamon.controller.tools.HttpClientHelper;
import cn.teamcat.doreamon.controller.tools.HttpClientHelperBasic;
import cn.teamcat.doreamon.controller.tools.SessionFactoryUtil;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

/**
 * GlobalConfig
 * 
 * @author Siyuan.Lu
 *
 */

public class GlobalConfig {
	public Integer splitCount;
	public Integer timerInterval;
	public Integer controllerInterval;
	public Integer agentDetcterInterval;
	public Integer disasterInterval;
	public Integer taskLimit;
	public Integer IssueInterval;
	public Integer IssueVersionlimited;
	
	public GlobalConfig() {				
		try {
			Integer EmailConfigtypeid = 24;
			JSONObject EmailConfigRsp = HttpClientHelperBasic.get(Constants.API.GET_DICCONFIG+EmailConfigtypeid+"/dicconfigs", null);
		    JSONArray result = EmailConfigRsp.getJSONArray("result");			
		for (int i = 0; i < result.size(); i++) {
			JSONObject data = result.getJSONObject(i);
			String dataName = data.getString("DicDataName");
			Integer dataValue = data.getInt("DicDataValue");
			if (dataName.equals("SplitCount")) {
				setSplitCount(dataValue);
				continue;
			}
			if (dataName.equals("TimerInterval")) {
				setTimerInterval(dataValue);	
				continue;
			}
			if (dataName.equals("ControllerInterval")) {
				setControllerInterval(dataValue);
				continue;
			}
			if (dataName.equals("AgentDetcterInterval")) {
				setAgentDetcterInterval(dataValue);	
				continue;
			}
			if (dataName.equals("DisasterInterval")) {
				setDisasterInterval(dataValue);	
				continue;
			}
			if (dataName.equals("TaskLimit")) {
				setTaskLimit(dataValue);	
				continue;
			}
			if (dataName.equals("IssueInterval")) {
				setIssueInterval(dataValue);		
				continue;
			}
			if (dataName.equals("IssueVersionlimited")) {
				setIssueVersionlimited(dataValue);		
				continue;
			}
		}
		} catch (Exception e) {
			// TODO: handle exception
		}
	}
	
	public Integer getSplitCount() {
		return splitCount;
	}
	public void setSplitCount(Integer splitCount) {
		this.splitCount = splitCount;
	}
	public Integer getTimerInterval() {
		return timerInterval;
	}
	public void setTimerInterval(Integer timerInterval) {
		this.timerInterval = timerInterval;
	}
	public Integer getControllerInterval() {
		return controllerInterval;
	}
	public void setControllerInterval(Integer controllerInterval) {
		this.controllerInterval = controllerInterval;
	}
	
	public Integer getAgentDetcterInterval() {
		return agentDetcterInterval;
	}
	public void setAgentDetcterInterval(Integer agentDetcterInterval) {
		this.agentDetcterInterval = agentDetcterInterval;
	}
	public Integer getDisasterInterval() {
		return disasterInterval;
	}
	public void setDisasterInterval(Integer disasterInterval) {
		this.disasterInterval = disasterInterval;
	}
	public Integer getTaskLimit() {
		return taskLimit;
	}
	public void setTaskLimit(Integer taskLimit) {
		this.taskLimit = taskLimit;
	}
	public void setIssueInterval(Integer IssueInterval) {
		this.IssueInterval = IssueInterval;
	}
	public Integer getIssueInterval() {
		return IssueInterval;
	}
	
	public void setIssueVersionlimited(Integer IssueVersionlimited) {
		this.IssueVersionlimited = IssueVersionlimited;
	}
	public Integer getIssueVersionlimited() {
		return IssueVersionlimited;
	}
}
