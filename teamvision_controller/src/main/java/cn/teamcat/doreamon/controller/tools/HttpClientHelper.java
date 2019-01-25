package cn.teamcat.doreamon.controller.tools;

import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Calendar;
import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.Set;

import javax.net.ssl.SSLContext;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

import org.apache.http.Header;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPatch;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpPut;
import org.apache.http.conn.ssl.SSLConnectionSocketFactory;
import org.apache.http.conn.ssl.TrustStrategy;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.protocol.HTTP;
import org.apache.http.util.EntityUtils;
import org.apache.log4j.Logger;
import com.meterware.httpunit.HttpUnitOptions;
import com.meterware.httpunit.PostMethodWebRequest;
import com.meterware.httpunit.WebConversation;
import com.meterware.httpunit.WebRequest;
import com.meterware.httpunit.javascript.JavaScript.Control;

import cn.teamcat.doraemon.controller.db.dict.DatasEnum;
import cn.teamcat.doreamon.controller.app.Launcher;
import cn.teamcat.doreamon.controller.config.GlobalConfig;
import cn.teamcat.doreamon.controller.flow.IssueStatistics;
import cn.teamcat.doreamon.controller.tools.HttpClientHelperBasic;;


/**
 * httpclient调用和json的解析
 * 
 * @author Sirui.Zhang,Siyuan.Lu
 *
 */
public class HttpClientHelper {

	private Logger log = Logger.getLogger(HttpClientHelper.class);
    CommonUtil time = new CommonUtil();
	public static CommonUtil util = new CommonUtil();
	/**
	 * 向消息队列下发消息
	 * 
	 * @param channel
	 * @param message
	 * @return
	 * @throws Exception
	 */
	public static JSONObject postMq(String channel, String message) throws Exception {
		JSONObject params = new JSONObject();
		params.put("channel", channel);
		params.put("message", message);
		System.out.println(channel);
		System.out.println(message);
		System.out.println(params);
		JSONObject actual = HttpClientHelperBasic.postobj(Constants.API.POST_SIMPLE_MQ, params);
		System.out.println(actual);
		return actual;
	}
	/**
	 * 获取所有project列表
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getProjectList()  throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_PROJECTLIST, params);
		return actual;
	}
	/**
	 * 根据StatisticsDate获取daily_statistics列表
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getdaily_statisticsbydate(String date,Integer projectid,Integer versionId)  throws Exception {
		Map<String, String> params = new HashMap<String, String>();
        params.put("StatisticsDate", date) ;
        params.put("ProjectID", projectid.toString());
        params.put("VersionID", versionId.toString());
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_DAILYSTATISTICSBYDATE, params);
		return actual;
	}
	/**
	 * 获取taskqueues列表
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject gettaskqueues()  throws Exception {
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_TASKQUEUES, null);
		return actual;
	}
	
	/**
	 * 根据id，command,taskuuid获取taskqueues列表
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public JSONObject gettaskqueuesbyid(Integer id,Integer command,String TaskUUID)  throws Exception {
		Map<String, String> params = new HashMap<String, String>();
        params.put("id", id.toString()) ;
        params.put("Command", command.toString());
        params.put("TaskUUID", TaskUUID);
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_TASKQUEUES, params);
		return actual;
	}
	
	/**
	 * 将taskqueues中某个task更新状态和错误信息
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public void updatetaskqueue(Integer taskQid,Integer Status,String ErrorMsg)  throws Exception {
		JSONObject jsonObj = new JSONObject();
        jsonObj.put("Status", Status);
        jsonObj.put("ErrorMsg", ErrorMsg);
        HttpClientHelperBasic.patchobj(Constants.API.PATCH_TASKQUEUE+"/"+taskQid, jsonObj);
	}
	/**
	 * 将taskqueues中某个task更新CaseList
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public void updatetaskqueueCaseList(Integer taskQid,String CaseList)  throws Exception {
		JSONObject jsonObj = new JSONObject();
        jsonObj.put("CaseList", CaseList);
        HttpClientHelperBasic.patchobj(Constants.API.PATCH_TASKQUEUE+"/"+taskQid, jsonObj);
	}
	
	/**
	 * 将taskqueues中某个task更新状态
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public void updatetaskqueueStatus(Integer taskQid,Integer Status)  throws Exception {
		JSONObject jsonObj = new JSONObject();
        jsonObj.put("Status", Status);
        HttpClientHelperBasic.patchobj(Constants.API.PATCH_TASKQUEUE+"/"+taskQid, jsonObj);
	}
	
	
	public void updatetaskqueueErr(Integer taskQid,String ErrorMsg)  throws Exception {
		JSONObject jsonObj = new JSONObject();
        jsonObj.put("ErrorMsg", ErrorMsg);
        HttpClientHelperBasic.patchobj(Constants.API.PATCH_TASKQUEUE+"/"+taskQid, jsonObj);
	}
	
	
	
	/**
	 * 更新taskresult by id
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public void updatetaskresultbyid(Integer taskresultid,Integer AgentId)  throws Exception {
		JSONObject jsonObj = new JSONObject();
        jsonObj.put("AgentID", AgentId);
        HttpClientHelperBasic.patchobj(Constants.API.PATCH_TASKQUEUE+"/"+taskresultid+"/", jsonObj);
	}
	/**
	 * 将taskqueues中某个task更新状态和错误信息
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public void updatetaskqueuebyid(Integer taskQid,Integer Status)  throws Exception {
		JSONObject jsonObj = new JSONObject();
        jsonObj.put("Status", Status);
        HttpClientHelperBasic.patchobj(Constants.API.PATCH_TASKQUEUE+"/"+taskQid, jsonObj);
	}
	
	/**
	 * 将taskqueues中某个task更新状态和错误信息
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public void updatetaskqueuebyidtime(Integer taskQid,String starttime,Integer Status)  throws Exception {
		JSONObject jsonObj = new JSONObject();
        jsonObj.put("Status", Status);
        jsonObj.put("StartTime", starttime);
        HttpClientHelperBasic.patchobj(Constants.API.PATCH_TASKQUEUE+"/"+taskQid, jsonObj);
	}
		
	/**
	 * 将taskqueues中某个task解锁
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject unlocktask(Integer id)  throws Exception {
		JSONObject jsonObj = new JSONObject();
        jsonObj.put("IsLocked", "false");
		JSONObject actual = HttpClientHelperBasic.patchobj(Constants.API.PATCH_TASKQUEUE+"/"+id, jsonObj);
		return actual;
	}
		
	/**
	 * 将taskqueues中某个task删除
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  void deletetask(Integer id)  throws Exception {
		HttpClientHelperBasic.deleteobj(Constants.API.PATCH_TASKQUEUE+"/"+id, null);
	}
	
	/**
	 * 根据taskUUId获取taskresults列表
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getTaskResultsbyTaskUUid(String taskuuid)  throws Exception {
		Map<String, String> params = new HashMap<String, String>();
        params.put("TaskUUID", taskuuid) ;
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_TASKRESULTS, params);
		return actual;
	}	
	/**
	 * 根据TaskResultID获取caseresults列表
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getCaseResultsbyTaskResultID(Integer TaskResultID,Integer Result)  throws Exception {
		Map<String, String> params = new HashMap<String, String>();
        params.put("TaskResultID", TaskResultID.toString()) ;
        params.put("Result", Result.toString()) ;
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_CASERESULTS, params);
		return actual;
	}	
	
	/**
	 * 根据taskqid删除taskqueue
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public void deleteTaskqueuebyid(Integer TaskQueueid)  throws Exception {
		if (TaskQueueid>0) {
	        HttpClientHelperBasic.delete(Constants.API.DELETETASKQUEUE+TaskQueueid);
		}
        System.out.println("delete TaskQueueid"+TaskQueueid);
	}	
	
	/**
	 * 根据Taskid获取ci_task列表
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getCItask(Integer Taskid)  throws Exception {
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_CITASK+"/"+Taskid+"/", null);
		return actual;
	}	
	
	/**
	 * 根据projectid获取project detail
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getProjectDetail(Integer projectid)  throws Exception {
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_PROJECTDETAIL+projectid+"/detail", null);
		return actual;
	}
	
	
	/**
	 * 根据Taskid和TaskQueueID获取task_histories列表
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getTaskhistories(Integer Taskid,Integer taskqid)  throws Exception {
		Map<String, String> params = new HashMap<String, String>();
        params.put("TaskQueueID", taskqid.toString()) ;
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_TASKHISTORIES+"api/ci/task/"+Taskid+"/task_histories", params);
		return actual;
	}	
	/**
	 * 根据historyid更新task_history结束时间
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	
	public  JSONObject updatetaskhistoryEndTime(Integer historyid)  throws Exception {
		JSONObject jsonObj = new JSONObject();  
				
		Calendar calendar = Calendar.getInstance(Locale.CHINA);
        Date now = calendar.getTime(); 
		SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS");
	    String runtimeString = String.valueOf(simpleDateFormat.format(now));	    
	    jsonObj.put("EndTime", runtimeString);
	    
		JSONObject actual = HttpClientHelperBasic.patchobj(Constants.API.PATCH_TASKHISTORY+"/"+historyid+"/", jsonObj);
		return actual;
	}
	
	/**
	 * 根据historyid更新task_history
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	
	public  JSONObject updatetaskhistory(Integer historyid,Integer BuildStatus,Integer TaskQueueID,String BuildMessage)  throws Exception {
		JSONObject jsonObj = new JSONObject();      
	    jsonObj.put("BuildStatus", BuildStatus);
	    jsonObj.put("TaskQueueID", TaskQueueID);
	    jsonObj.put("BuildMessage", BuildMessage);
		JSONObject actual = HttpClientHelperBasic.patchobj(Constants.API.PATCH_TASKHISTORY+"/"+historyid+"/", jsonObj);
		return actual;
	}
    
	
	/**
	 * 根据historyid更新task_history
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	
	public  JSONObject updatetaskhistorytimeagentid(Integer historyid,String StartTime,Integer AgentID)  throws Exception {
		JSONObject jsonObj = new JSONObject();      
	    jsonObj.put("StartTime", StartTime);
	    jsonObj.put("AgentID", AgentID);
		JSONObject actual = HttpClientHelperBasic.patchobj(Constants.API.PATCH_TASKHISTORY+"/"+historyid+"/", jsonObj);
		return actual;
	}
	
	/**
	 * 根据historyid更新task_history
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	
	public  JSONObject updatetaskhistoryTqid(Integer historyid,Integer TaskQueueID)  throws Exception {
		JSONObject jsonObj = new JSONObject();      
	    jsonObj.put("TaskQueueID", TaskQueueID);
		JSONObject actual = HttpClientHelperBasic.patchobj(Constants.API.PATCH_TASKHISTORY+"/"+historyid+"/", jsonObj);
		return actual;
	}

	
	/**
	 * 根据TaskResultID更新caseresult
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject updatecaseresult(Integer Total,Integer Pass,Integer Fail,Integer Aborted,String Errormassge,Integer Resultid)  throws Exception {
		JSONObject jsonObj = new JSONObject();
        jsonObj.put("Total", Total);
        jsonObj.put("Pass", Pass);
        jsonObj.put("Fail", Fail);
        jsonObj.put("Aborted", Aborted);
        jsonObj.put("BuildMessage", Errormassge);
		JSONObject actual = HttpClientHelperBasic.patchobj(Constants.API.PATCH_TASKRESULT+"/"+Resultid+"/", jsonObj);
		return actual;
	}
	
	
	
	
	
	 
	/**
	 * 根据Status和IsLocked获取Locked taskqueues列表
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getLockedTaskqueues()  throws Exception {
		Map<String, String> params = new HashMap<String, String>();
        params.put("Status!", String.valueOf(DatasEnum.TaskInQueueStatus_Disaster.getValue())) ;
        params.put("IsLocked", "true");
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_TASKQUEUES, params);
		return actual;
	}
	/**
	 * 获取version_statistics列表
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getdversion_statisticsbyDimbyDimvalue(Integer projectid,Integer versionId,Integer Dimension,Integer DimensionValue )  throws Exception {
		Map<String, String> params = new HashMap<String, String>();
        params.put("ProjectID", projectid.toString());
        params.put("VersionID", versionId.toString());
        params.put("Dimension", Dimension.toString());
        params.put("DimensionValue", DimensionValue.toString());
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_VERSIONSTATISTICSBY, params);
		return actual;
	}
	
	/**
	 * 获取某个agent上正在运行的测试任务列表
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getrunning_testtypelist(Integer AgentID)  throws Exception {
		Map<String, String> params = new HashMap<String, String>();
        params.put("Status", String.valueOf(DatasEnum.TaskInQueueStatus_Running.getValue()));
        params.put("AgentID", AgentID.toString());
        params.put("TaskType",String.valueOf(DatasEnum.TaskType_Interface.getValue()) );
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_TASKQUEUES, params);
		return actual;
	}
	
	/**
	 * 获取某个ci_task表信息	
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getci_tasklist()  throws Exception {
		Map<String, String> params = new HashMap<String, String>();
        params.put("page_size","1000");
        params.put("Schedule__isnull!", null);
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_CITASKLIST, params);
		return actual;
	}
	
	/**
	 * 根据taskid获取某个ci_task表信息	
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getci_tasklistbytaskid(Integer taskId)  throws Exception {
    	JSONObject response = HttpClientHelperBasic.get(Constants.API.CITASBASIC + taskId + "/", null);
		return response;
	}
	

	
	/**
	 * 获取issue_severities列表
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getissue_severities()  throws Exception {
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_SEVERITIES, null);
		return actual;
	}
	/**
	 * 获取issue_catergories列表
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getissue_catergories()  throws Exception {
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_CATERGORIES, null);
		return actual;
	}
	/**
	 * 获取issue_resolvedtypes列表
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getissue_resolvedtypes()  throws Exception {
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_RESOLVETYPES, null);
		return actual;
	}
	/**
	 * 获取issue_projectmodule列表
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getissue_projectmodule(Integer projectid)  throws Exception {
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_PROJECT+"/"+projectid+"/project_modules", null);
		return actual;
	}
	
	/**
	 * 获取section中task列表
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getsectionTasks(Integer sectionid)  throws Exception {
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_SECTIONTASKS+sectionid, null);
		return actual;
	}
	
	/**
	 * 获取taskflow中section列表
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getTaskflowSections(Integer taskflowid)  throws Exception {
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_TASKFLOW+taskflowid+"/sections", null);
		return actual;
	}
	
	
	
	
	
	
	
	
	/**
	 * 根据projectid，versionid,date获取projectissue列表
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getProjectIssuebyIdVersiondate(Integer id,Integer version,String daterange)  throws Exception {
		Map<String, String> params = new HashMap<String, String>();
        params.put("CreationTime__range", daterange) ;
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_PROJECT+"/"+id+"/"+version+"/issues", params);
		return actual;
	}
	
	/**
	 * 根据projectid，versionid,获取projectissue列表
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getProjectIssuebyIdVersion(Integer id,Integer version)  throws Exception {
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_PROJECT+"/"+id+"/"+version+"/issues", null);
		return actual;
	}
	
	/**
	 * 获取projectissueStatus列表
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getProjectIssueStatus()throws Exception {
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_PROJECTISSUESTATUS, null);
		return actual;
	}
	
	
	/**
	 * 根据projectid获取version列表
	 * 
	 * @param 
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getProjectVersionList(Integer id)  throws Exception {
	
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_PROJECT_VERSION+id+"/versions", null);
		return actual;
	}
	
	/**
	 * 获取在线agents列表
	 * 
	 * @param Status_Offline
	 * @return
	 * @throws Exception
	 */
	public  JSONObject getAgentOnline()  throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		String agentStatus_Offline = String.valueOf(DatasEnum.AutoAgentStatus_Offline.getValue());
		params.put("Status!", agentStatus_Offline);
		log.info("agentStatus_Offline"+agentStatus_Offline);
		log.info("params"+params);
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_AGENTS, params);
		log.info(actual);
		return actual;
	}
	
	/**
	 * 获取某固定agentId上的taskqueuesId
	 * 
	 * @param agentId
	 * @return
	 * @throws Exception
	 */
	public JSONObject getTaskqueuesId(Integer agentId) throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		params.put("AgentID", agentId.toString());
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_TASKQUEUES, params);
		return actual;
	}
	
	/**
	 * 判断section中其他任务是否结束
	 * 
	 * @param agentId
	 * @return
	 * @throws Exception
	 */
	public JSONObject getTaskqueuesbyuuidandTasktype(String uuid) throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		params.put("TaskType__in",  String.valueOf(DatasEnum.TaskType_Interface.getValue())+","+String.valueOf(DatasEnum.TaskType_WebUI.getValue())+","+String.valueOf(DatasEnum.TaskType_APPUI.getValue())+","+String.valueOf(DatasEnum.TaskType_Build.getValue())+","+String.valueOf(DatasEnum.TaskType_Deploy.getValue()));
		params.put("TaskUUID__contains", uuid);
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_TASKQUEUES, params);
		return actual;
	}
	
	/**
	 * 判断taskflow中其他section是否结束
	 * 
	 * @param agentId
	 * @return
	 * @throws Exception
	 */
	public JSONObject getSectionTaskqueuesbyuuidandTasktype(String uuid) throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		params.put("TaskType",  String.valueOf(DatasEnum.TaskType_Taskflow.getValue()));
		params.put("TaskUUID__contains", uuid);
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_TASKQUEUES, params);
		return actual;
	}
	
	
	/**
	 * 获取section或者taskflow tqid
	 * 
	 * @param agentId
	 * @return
	 * @throws Exception
	 */
	public Integer getTaskfloworSectionTqid(String uuid,Integer Tasktype) throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		params.put("TaskType",  String.valueOf(Tasktype));
		params.put("TaskUUID__contains", uuid);
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_TASKQUEUES, params);
		if (actual.getJSONArray("result").size()>0) {
			return actual.getJSONArray("result").getJSONObject(0).getInt("id");
		}else {
			return 0;
		}
	}
	
	
	/**
	 * 获取某固定Status的taskqueues列表
	 * 
	 * @param Status
	 * @return
	 * @throws Exception
	 */
	public JSONObject getTaskqueuesbyStatus(Integer Status) throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		params.put("Status", Status.toString());
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_TASKQUEUES, params);
		return actual;
	}
	
	/**
	 * 获取某固定taskuuid和command的taskqueues列表
	 * 
	 * @param Status
	 * @return
	 * @throws Exception
	 */
	public JSONObject getTaskqueuesbyuuidandCommand(String TaskUUID,Integer Command) throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		params.put("TaskUUID", TaskUUID);
		params.put("Command", Command.toString());
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_TASKQUEUES, params);
		return actual;
	}
	
	
	
	
	/**
	 * 将固定agentId状态下线
	 * 
	 * @param agentId
	 * @return
	 * @throws Exception
	 */
	public Integer setofflineagentId(Integer agentId) throws Exception {
		JSONObject jsonObj = new JSONObject();
		jsonObj.put("Status", DatasEnum.AutoAgentStatus_Offline.getValue());
		JSONObject actual = HttpClientHelperBasic.patchobj(Constants.API.SETOFFLINEAGENTID+"/"+agentId, jsonObj);
		return actual.getInt("code");
	}
	/**
	 * 更新taskqueue
	 * 
	 * @param taskqueueId
	 * @return
	 * @throws Exception
	 */
	public Integer setstatustaskqueueId(Integer taskqueueId,Integer Status) throws Exception {
		JSONObject jsonObj = new JSONObject();
		jsonObj.put("Status", Status);
		JSONObject actual = HttpClientHelperBasic.patchobj(Constants.API.SETOFFLINETASKQUEUES+"/"+taskqueueId, jsonObj);
		return actual.getInt("code");
	}
	/**
	 * 更新taskqueue
	 * 
	 * @param taskqueueId
	 * @return
	 * @throws Exception
	 */
	public void setstatusagentidbytaskqueueId(Integer taskqueueId,Integer Status,Integer AgentId) throws Exception {
		JSONObject jsonObj = new JSONObject();
		jsonObj.put("Status", Status);
		jsonObj.put("AgentID", AgentId);	
		HttpClientHelperBasic.patchobj(Constants.API.SETOFFLINETASKQUEUES+"/"+taskqueueId, jsonObj);
	}
	
	/**
	 * 将固定taskqueueId设置错误状态
	 * 
	 * @param agentId
	 * @return
	 * @throws Exception
	 */
	public Integer seterrormsgtaskqueueId(Integer taskqueueId,String errormsg) throws Exception {
		JSONObject jsonObj = new JSONObject();
		jsonObj.put("ErrorMsg", errormsg);
		JSONObject actual = HttpClientHelperBasic.patchobj(Constants.API.SETOFFLINETASKQUEUES+"/"+taskqueueId, jsonObj);
		return actual.getInt("code");
	}
    
	/**
	 * 将固定taskqueueId设置其他状态
	 * 
	 * @param agentId
	 * @return
	 * @throws Exception
	 */
	public Integer setstatusstaskqueueId(Integer taskqueueId,Integer status) throws Exception {
		JSONObject jsonObj = new JSONObject();
		jsonObj.put("Status", status.toString());
		JSONObject actual = HttpClientHelperBasic.patchobj(Constants.API.SETOFFLINETASKQUEUES+"/"+taskqueueId, jsonObj);
		return actual.getInt("code");
	}
	
	/**
	 * 插入TaskFlowHistory
	 * 
	 * @param taskflowid taskQueue
	 * @return
	 * @throws Exception
	 */
	public Integer insertCITaskFlowHistory(Integer taskflowid,JSONObject taskQueue,Integer fromname) throws Exception {
		JSONObject jsonObj = new JSONObject();
		Date now =  util.getUTCDate();
		SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS");
	    String runtimeString = String.valueOf(simpleDateFormat.format(now));
		jsonObj.put("StartTime", runtimeString+"+00:00");
		jsonObj.put("TaskFlow", taskflowid);
		jsonObj.put("StartedBy", fromname);
		jsonObj.put("Status", taskQueue.getInt("Status"));
		jsonObj.put("TQUUID", taskQueue.getString("TaskUUID"));
		JSONObject actual = HttpClientHelperBasic.postobj(Constants.API.POST_TASKFLOWHISTORYURL+"/"+taskflowid+"/history/list", jsonObj);
		return actual.getJSONObject("result").getInt("id");
	}
				
	/**
	 * 插入TaskSectionHistory
	 * 
	 * @param  taskflow historyid taskflowid Sectionid taskQueue
	 * @return
	 * @throws Exception
	 */
	public Integer insertCITaskSectionHistory(Integer taskflowhistoryid,Integer taskflowid,Integer Sectionid ,JSONObject taskQueue,Integer fromname) throws Exception {
		JSONObject jsonObj = new JSONObject();
		Date now =  util.getUTCDate();
		SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS");
	    String runtimeString = String.valueOf(simpleDateFormat.format(now));
		jsonObj.put("StartTime", runtimeString+"+00:00");
		jsonObj.put("TaskFlow", taskflowid);
		jsonObj.put("Status", taskQueue.getInt("Status"));
		jsonObj.put("StartedBy", fromname);
		jsonObj.put("TQUUID", taskQueue.getString("TaskUUID"));
		jsonObj.put("TaskFlowHistory", taskflowhistoryid);
		jsonObj.put("Section", Sectionid);
		JSONObject actual = HttpClientHelperBasic.postobj(Constants.API.POST_TASKFLOWSECTIONHISTORYURL+"/"+taskflowhistoryid+"/section_history/list", jsonObj);
	    return actual.getJSONObject("result").getInt("id");
	}
	
	/**
	 * 获取CITaskFlowHistory
	 * 
	 * @param agentId
	 * @return
	 * @throws Exception
	 */
	public JSONObject getCITaskFlowHistoryId(Integer taskflowid,String taskuuid) throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		params.put("TQUUID__icontains", taskuuid);
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.POST_TASKFLOWHISTORYURL+taskflowid+"/history/list", params);
		return actual;
	}
	
	
	/**
	 * 获取CITaskSectionHistory
	 * 
	 * @param Status
	 * @return
	 * @throws Exception
	 */
	public JSONObject getCITaskSectionHistoryId(Integer taskflowhistoryid,String taskuuid,Integer SectionId) throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		params.put("TQUUID__icontains", taskuuid);
		params.put("Section", String.valueOf(SectionId));
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.POST_TASKFLOWSECTIONHISTORYURL+taskflowhistoryid+"/section_history/list", params);
		return actual;
	}
	
	/**
	 * 获取CITaskSectionHistory
	 * 
	 * @param Status
	 * @return
	 * @throws Exception
	 */
	public JSONObject getCITaskSectionHistoryIdbyStatus(Integer taskflowhistoryid,String taskuuid,Integer Status) throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		params.put("TQUUID__icontains", taskuuid);
		params.put("Status!", String.valueOf(Status));
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.POST_TASKFLOWSECTIONHISTORYURL+taskflowhistoryid+"/section_history/list", params);
		return actual;
	}
	
	/**
	 * 更新TaskFlowHistory
	 * 
	 * @param taskflowid status
	 * @return
	 * @throws Exception
	 */
	public void updateCITaskFlowHistory(Integer taskflowhistoryid,Integer Status) throws Exception {
		JSONObject jsonObj = new JSONObject();
		Date now =  util.getUTCDate();
		SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS");
	    String runtimeString = String.valueOf(simpleDateFormat.format(now));
		jsonObj.put("EndTime", runtimeString+"+00:00");
		jsonObj.put("Status", Status);
		HttpClientHelperBasic.patchobj(Constants.API.POST_TASKFLOWSECTIONHISTORYURL+taskflowhistoryid+"/", jsonObj);
	}
	
	
	/**
	 * 更新TaskSectionHistory
	 * 
	 * @param  Status 
	 * @return
	 * @throws Exception
	 */
	public void updateCITaskSectionHistory(Integer taskflowsectionhistoryid) throws Exception {
		JSONObject jsonObj = new JSONObject();
		Date now =  util.getUTCDate();
		SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS");
	    String runtimeString = String.valueOf(simpleDateFormat.format(now));
		jsonObj.put("EndTime", runtimeString+"+00:00");
	    HttpClientHelperBasic.patchobj(Constants.API.POST_TASKFLOWSECTIONHISTORYIDURL+taskflowsectionhistoryid, jsonObj);
	}

	/**
	 * 更新TaskFlowHistory
	 * 
	 * @param taskflowid status
	 * @return
	 * @throws Exception
	 */
	public void updateCITaskFlowHistory(Integer taskflowhistoryid ) throws Exception {
		JSONObject jsonObj = new JSONObject();
		Date now =  util.getUTCDate();
		SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS");
	    String runtimeString = String.valueOf(simpleDateFormat.format(now));
		jsonObj.put("EndTime", runtimeString+"+00:00");
		HttpClientHelperBasic.patchobj(Constants.API.POST_TASKFLOWSECTIONHISTORYURL+taskflowhistoryid+"/", jsonObj);
	}
	
	
	/**
	 * 更新TaskSectionHistory
	 * 
	 * @param  Status 
	 * @return
	 * @throws Exception
	 */
	public void updateCITaskSectionHistory(Integer taskflowsectionhistoryid,Integer Status) throws Exception {
		JSONObject jsonObj = new JSONObject();
		Date now =  util.getUTCDate();
		SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS");
	    String runtimeString = String.valueOf(simpleDateFormat.format(now));
		jsonObj.put("EndTime", runtimeString+"+00:00");
		jsonObj.put("Status", Status);
	    HttpClientHelperBasic.patchobj(Constants.API.POST_TASKFLOWSECTIONHISTORYIDURL+taskflowsectionhistoryid, jsonObj);
	}
	

	
	
	
	/**
	 * 获取在线agentlist
	 * 
	 * @param taskId
	 * @param taskType
	 * @return
	 * @throws Exception
	 */
	public JSONObject getonlineagentlist(Integer Status) throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		params.put("task_type", Status.toString());
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_AGENTS, params);
		return actual;
	}	
	
	/**
	 * 获取任务详情
	 * 
	 * @param taskId
	 * @param taskType
	 * @return
	 * @throws Exception
	 */
	public JSONObject getTaskInfo(Integer taskId, Integer taskType) throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		params.put("task_id", taskId.toString());
		params.put("task_type", taskType.toString());
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_TASK, params);
		return actual.getJSONObject("result");
	}

	/**
	 * 获取CI任务配置信息
	 * 
	 * @param taskQueue
	 * @return
	 * @throws Exception
	 */
	public Map<String, String> getCITaskConfig( JSONObject taskQueue) throws Exception {
		Map<String, String> basic = new HashMap<String, String>();
		JSONObject result = getTaskInfo(taskQueue.getInt("TaskID"), taskQueue.getInt("TaskType"));
		JSONArray plugins = result.getJSONObject("task_config").getJSONObject("basic_section").getJSONArray("plugins");
		if (plugins.size() > 0) {
			JSONArray parameter = plugins.getJSONObject(0).getJSONArray("parameter");
			for (int i = 0; i < parameter.size(); i++) {
				JSONObject obj = parameter.getJSONObject(i);
				basic.put(obj.getString("name"), obj.getString("value"));
			}

		}
		return basic;
	}
	
	/**
	 * 获取agent信息
	 * 
	 * @param agentid
	 * @return
	 * @throws Exception
	 */
	public JSONObject getAgentbyid(Integer agentid) throws Exception {
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_AGENT+"/"+agentid, null);
		JSONObject result = actual.getJSONObject("result");
		return result;
	}
	
	/**
	 * 获取agent上的任务列表
	 * 
	 * @param agentid
	 * @return
	 * @throws Exception
	 */
	public JSONArray getTaskQbyagentid(Integer agentid,Integer command) throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		params.put("AgentID", agentid.toString());
		params.put("Command", command.toString());
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_TASKQUEUES, params);
		JSONArray result = actual.getJSONArray("result");
		return result;
	}
	
	public JSONArray getappointTask(Integer tasktype,Integer taskid,Integer agentid,Integer command ) throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		params.put("TaskType", tasktype.toString());
		params.put("TaskID", taskid.toString());
		params.put("AgentID", agentid.toString());
		params.put("Command", command.toString());
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_TASKQUEUES, params);
		JSONArray result = actual.getJSONArray("result");
		return result;
	}
	
	/**
	 * 获取IssueStatus
	 * 
	 * @param projectId,Status
	 * @return
	 * @throws Exception
	 */
	public Integer getCreatedStatus() throws Exception {
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_PROJECTISSUESTATUS,null);
		Integer CreatedStatus = actual.getJSONArray("result").getJSONObject(0).getInt("Value");
		return CreatedStatus;
	}
    public Integer getClosedStatus() throws Exception {
    	    JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_PROJECTISSUESTATUS,null);
		Integer ClosedStatus = actual.getJSONArray("result").getJSONObject(2).getInt("Value");
		return ClosedStatus;
		
	}
    public Integer getFixedStatus() throws Exception {
    	    JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_PROJECTISSUESTATUS,null);
		Integer FixedStatus = actual.getJSONArray("result").getJSONObject(3).getInt("Value");
		return FixedStatus;
		
	}
    
	/**
	 * 获取agent上面所有运行的任务列表
	 * 
	 * @param taskQueue
	 * @return
	 * @throws Exception
	 */
	public ArrayList<Integer> getAgentTaskid(Integer agentid) throws Exception {
		ArrayList<Integer> takid = new ArrayList<>();
		Map<String, String> params = new HashMap<String, String>();
		params.put("AgentID", agentid.toString());
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_AGENTTASK, params);
		JSONArray result = actual.getJSONArray("result");
		for (int i = 0; i < result.size(); i++) {
			takid.add(result.getJSONObject(i).getInt("TaskID"));
		}
		return takid;
	}

	
	/**
	 * 获取dailyIssueStatistic
	 * 
	 * @param projectId,Status
	 * @return
	 * @throws Exception
	 */
	 public Integer getOpenedTotal(Integer projectid,Integer projectversion) throws Exception {
		 Map<String, String> params = new HashMap<String, String>();
		 Integer CreatedStatus=getCreatedStatus();
		 params.put("Status!", CreatedStatus.toString());
		 JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_PROJECT +"/"+projectid + "/"+projectversion+"/"+"issues", params);
		 JSONArray result = actual.getJSONArray("result");
		 Integer OpenedTotalCounts = result.size();
		 return OpenedTotalCounts;
	}
	 public Integer getClosedTotal(Integer projectid,Integer projectversion) throws Exception {
		 Map<String, String> params = new HashMap<String, String>();
		 Integer ClosedStatus=getClosedStatus();
		 params.put("Status", ClosedStatus.toString());
		 JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_PROJECT +"/"+projectid + "/"+projectversion+"/"+"issues", params);
		 JSONArray result = actual.getJSONArray("result");
		 Integer ClosedTotalCounts = result.size();
		 return ClosedTotalCounts;
	}
	 public Integer getFixedTotal(Integer projectid,Integer projectversion) throws Exception {
		 Map<String, String> params = new HashMap<String, String>();
		 Integer ClosedStatus=getClosedStatus();
		 Integer FixedStatus=getFixedStatus();
		 params.put("Status__in", ClosedStatus.toString()+","+FixedStatus.toString());
		 JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_PROJECT +"/"+projectid + "/"+projectversion+"/"+"issues", params);
		 JSONArray result = actual.getJSONArray("result");
		 Integer FixedTotalCounts = result.size();
		 return FixedTotalCounts;
	}
	 public Integer getOpenedToday(Integer projectid,Integer projectversion) throws Exception {
		 Map<String, String> params = new HashMap<String, String>();
         String tomorrow = time.getUTCTimeStr(1);
         String today = time.getUTCTimeStr(0);
		 Integer CreatedStatus=getCreatedStatus();
		 params.put("CreationTime__range", today+","+tomorrow);
		 params.put("Status!", CreatedStatus.toString());
		 log.info("++++++++++++++++++++++++++++ResolvedTime__range"+today+tomorrow);
		 JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_PROJECT +"/"+projectid + "/"+projectversion+"/"+"issues", params);
		 JSONArray result = actual.getJSONArray("result");
		 Integer OpenedTodayCounts = result.size();
		 return OpenedTodayCounts;
	}
	 public Integer getFixedToday(Integer projectid,Integer projectversion) throws Exception {
		 Map<String, String> params = new HashMap<String, String>();
         String today = time.getUTCTimeStr(0);
         String tomorrow = time.getUTCTimeStr(1);
		 Integer ClosedStatus=getClosedStatus();
		 Integer FixedStatus=getFixedStatus();
		 params.put("ResolvedTime__range", today+","+tomorrow);
		 params.put("Status__in", ClosedStatus.toString()+","+FixedStatus.toString());
		 log.info("++++++++++++++++++++++++++++ResolvedTime__range"+today+tomorrow);
		 JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_PROJECT +"/"+projectid + "/"+projectversion+"/"+"issues", params);
		 JSONArray result = actual.getJSONArray("result");
		 Integer OpenedTodayCounts = result.size();
		 return OpenedTodayCounts;
	}
	 public Integer getReopenedToday(Integer projectid,Integer projectversion) throws Exception {
		 JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_PROJECT +"/"+projectid + "/"+projectversion+"/"+"issues", null);
		 JSONArray result = actual.getJSONArray("result");
		 Integer ReopenedCounts = 0;
		 for (int i = 0; i < result.size(); i++) {
			ReopenedCounts+=result.getJSONObject(i).getInt("ReopenCounts");
		}
		 return ReopenedCounts;
	}

	/**
	 * dailyStatistics insert
	 * 
	 * @param projectid,projectversion
	 * @return
	 * @throws Exception
	 */
	public void dailyStatisticsinsert(Integer projectid, Integer projectversion) throws Exception {
		JSONObject jsonObj = new JSONObject();
		ArrayList<Object> parameterskeyList = new ArrayList<Object>();
		parameterskeyList.clear();
		String[] parameterskey = { "ProjectID", "OpenedTotal", "FixedTotal", "OpenedToday", "VersionID",
				"StatisticsDate", "ReopenedToday", "FixedToday", "ClosedTotal" };
		Collections.addAll(parameterskeyList, parameterskey);
		log.info("+++++parameterskeyList+++++++++" + parameterskeyList);
		String ProjecID = projectid.toString();
		String OpenedTotal = getOpenedTotal(projectid, projectversion).toString();
		String FixedTotal = getFixedTotal(projectid, projectversion).toString();
		String OpenedToday = getOpenedToday(projectid, projectversion).toString();
		String VersionID = projectversion.toString();
		String StatisticsDate = time.getUTCTimeStr(0);
		String ReopenedToday = getReopenedToday(projectid, projectversion).toString();
		String FixedToday = getFixedToday(projectid, projectversion).toString();
		String ClosedTotal = getClosedTotal(projectid, projectversion).toString();
		String[] parametersvalue = { ProjecID, OpenedTotal, FixedTotal, OpenedToday, VersionID, StatisticsDate,
				ReopenedToday, FixedToday, ClosedTotal };
		ArrayList<Object> parametersvalueList = new ArrayList<Object>();
		parametersvalueList.clear();
		Collections.addAll(parametersvalueList, parametersvalue);
		log.info("+++++parameterskeyList+++++++++" + parametersvalueList);
		if (parameterskeyList.size() > 0) {
			for (int i = 0; i < parameterskeyList.size(); i++) {
				String jsonKey = parameterskeyList.get(i).toString();
				jsonObj.put(jsonKey, parametersvalueList.get(i));
			}
		}
		HttpClientHelperBasic.postobj(Constants.API.POST_DAILY_STATISTICS, jsonObj);
	}
	/**
	 * dailyStatistics update
	 * 
	 * @param projectid,projectversion
	 * @return
	 * @throws Exception
	 */
	
	
	public void dailyStatisticsupdate(Integer projectid, Integer projectversion,Integer id) throws Exception {
		JSONObject jsonObj = new JSONObject();
		ArrayList<Object> parameterskeyList = new ArrayList<Object>();
		parameterskeyList.clear();
		String[] parameterskey = { "ProjectID", "OpenedTotal", "FixedTotal", "OpenedToday", "VersionID",
				"StatisticsDate", "ReopenedToday", "FixedToday", "ClosedTotal" };
		Collections.addAll(parameterskeyList, parameterskey);
		log.info("+++++++parameterskeyList+++++++" + parameterskeyList);
		String ProjecID = projectid.toString();
		String OpenedTotal = getOpenedTotal(projectid, projectversion).toString();
		String FixedTotal = getFixedTotal(projectid, projectversion).toString();
		String OpenedToday = getOpenedToday(projectid, projectversion).toString();
		String VersionID = projectversion.toString() ;
		String StatisticsDate = time.getUTCTimeStr(0);
		String ReopenedToday = getReopenedToday(projectid, projectversion).toString();
		String FixedToday = getFixedToday(projectid, projectversion).toString();
		String ClosedTotal = getClosedTotal(projectid, projectversion).toString();
		String[] parametersvalue = { ProjecID, OpenedTotal, FixedTotal, OpenedToday, VersionID, StatisticsDate,
				ReopenedToday, FixedToday, ClosedTotal };
		ArrayList<Object> parametersvalueList = new ArrayList<Object>();
		parametersvalueList.clear();
		Collections.addAll(parametersvalueList, parametersvalue);
		log.info("++++++++parameterskeyList++++++" + parametersvalueList);
		if (parameterskeyList.size() > 0) {
			for (int i = 0; i < parameterskeyList.size(); i++) {
				String jsonKey = parameterskeyList.get(i).toString();
				jsonObj.put(jsonKey, parametersvalueList.get(i));
			}
		}
		HttpClientHelperBasic.patchobj(Constants.API.POST_DAILY_STATISTICS+"/"+id, jsonObj);
	}
	
	public Integer getIssuetotalbyseverity(Integer projectid, Integer projectversion,Integer DimensionValues) throws Exception{
		Map<String, String> params = new HashMap<String, String>();
        params.put("Severity", DimensionValues.toString()) ;
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_PROJECT+"/"+projectid+"/"+projectversion+"/issues", params);
		Integer issuetotal = actual.getJSONArray("result").size();
		return issuetotal;
	}
	
    public Integer getIssuetotalbyCategory(Integer projectid, Integer projectversion, Integer DimensionValues) throws Exception{
      	Map<String, String> params = new HashMap<String, String>();
        params.put("IssueCategory", DimensionValues.toString()) ;
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_PROJECT+"/"+projectid+"/"+projectversion+"/issues", params);
		Integer issuetotal = actual.getJSONArray("result").size();
		return issuetotal;
	}

    public Integer getIssuetotalbyResolvedType(Integer projectid, Integer projectversion,Integer DimensionValues) throws Exception{
      	Map<String, String> params = new HashMap<String, String>();
        params.put("Solution", DimensionValues.toString()) ;
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_PROJECT+"/"+projectid+"/"+projectversion+"/issues", params);
		Integer issuetotal = actual.getJSONArray("result").size();
		return issuetotal;
	}
    
    public Integer getIssuetotalbyModule(Integer projectid, Integer projectversion,Integer DimensionValues) throws Exception {
     	Map<String, String> params = new HashMap<String, String>();
        params.put("Module", DimensionValues.toString()) ;
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_PROJECT+"/"+projectid+"/"+projectversion+"/issues", params);
		Integer issuetotal = actual.getJSONArray("result").size();
		return issuetotal;
	}
	
	
	
	
	
	
	
	/**
	 * getIssueTotalbyDimbyDimValues
	 * 根据不同维度从projectissue中拿出需要的bug数量
	 * @param projectid,projectversion,Dimensions,DimensionValues
	 * @return
	 * @throws Exception
	 */ 
	
	public Integer getIssueTotalbyDimbyDimValues(Integer projectid, Integer projectversion,Integer Dimensions, Integer DimensionValues) throws Exception {
		Integer IssueTotal = 0 ;
		switch (Dimensions) {
		case 1:
			IssueTotal=getIssuetotalbyseverity(projectid,projectversion,DimensionValues);
			break;

        case 2:
           	IssueTotal=getIssuetotalbyCategory(projectid,projectversion,DimensionValues);
			break;
		
        case 3:
          	IssueTotal=getIssuetotalbyResolvedType(projectid,projectversion,DimensionValues); 
			break;
			
        case 4:
         	IssueTotal=getIssuetotalbyModule(projectid,projectversion,DimensionValues);
	        break;
		}
        return IssueTotal;
	}
	
	/**
	 * dailyStatistics insert
	 * 
	 * @param projectid,projectversion
	 * @return
	 * @throws Exception
	 */
	public void versionStatisticsinsert(Integer projectid, Integer projectversion,Integer Dimensions , Integer DimensionValues) throws Exception {
		JSONObject jsonObj = new JSONObject();
		ArrayList<Object> parameterskeyList = new ArrayList<Object>();
		parameterskeyList.clear();
		String[] parameterskey = { "ProjectID","StatisticsDate","IssueTotal","DimensionValue","VersionID","Dimension"};
		Collections.addAll(parameterskeyList, parameterskey);
		log.info("++++++++parametersvalueList++++++" + parameterskeyList);
		String ProjecID = projectid.toString();
		String StatisticsDate = time.getUTCTimeStr(0);
		String IssueTotal = getIssueTotalbyDimbyDimValues(projectid,projectversion,Dimensions,DimensionValues).toString();
		String DimensionValue = DimensionValues.toString();
		String VersionID = projectversion.toString();
		String Dimension = Dimensions.toString();
		String[] parametersvalue = { ProjecID, StatisticsDate, IssueTotal, DimensionValue, VersionID, Dimension };
		ArrayList<Object> parametersvalueList = new ArrayList<Object>();
		parametersvalueList.clear();
		Collections.addAll(parametersvalueList, parametersvalue);
		log.info("+++++++parametersvalueList+++++++" + parametersvalueList);
		if (parameterskeyList.size() > 0) {
			for (int i = 0; i < parameterskeyList.size(); i++) {
				String jsonKey = parameterskeyList.get(i).toString();
				jsonObj.put(jsonKey, parametersvalueList.get(i));
			}
		}
		HttpClientHelperBasic.postobj(Constants.API.POST_VERSION_STATISTICS, jsonObj);
	}
	
	/**
	 * dailyStatistics update
	 * 
	 * @param projectid,projectversion
	 * @return
	 * @throws Exception
	 */
	
	
	public void versionStatisticsupdate(Integer projectid, Integer projectversion,Integer id,Integer Dimensions , Integer DimensionValues) throws Exception {
		JSONObject jsonObj = new JSONObject();
		ArrayList<Object> parameterskeyList = new ArrayList<Object>();
		parameterskeyList.clear();
		String[] parameterskey = { "ProjectID","StatisticsDate","IssueTotal","DimensionValue","VersionID","Dimension"};
		Collections.addAll(parameterskeyList, parameterskey);
		log.info("+++++++parameterskeyList+++++++" + parameterskeyList);
		String ProjecID = projectid.toString();
		String StatisticsDate = time.getUTCTimeStr(0);
		String IssueTotal = getIssueTotalbyDimbyDimValues(projectid,projectversion,Dimensions,DimensionValues).toString();
		String DimensionValue = DimensionValues.toString();
		String VersionID = projectversion.toString();
		String Dimension = Dimensions.toString();
		String[] parametersvalue = { ProjecID, StatisticsDate, IssueTotal, DimensionValue, VersionID, Dimension };
		ArrayList<Object> parametersvalueList = new ArrayList<Object>();
		parametersvalueList.clear();
		Collections.addAll(parametersvalueList, parametersvalue);
		log.info("+++++++parameterskeyList+++++++" + parametersvalueList);
		if (parameterskeyList.size() > 0) {
			for (int i = 0; i < parameterskeyList.size(); i++) {
				String jsonKey = parameterskeyList.get(i).toString();
				jsonObj.put(jsonKey, parametersvalueList.get(i));
			}
		}
		HttpClientHelperBasic.patchobj(Constants.API.POST_VERSION_STATISTICS+"/"+id, jsonObj);
	}
	 
	/**
	 * 获取用户列表
	 * 
	 * @param projectId
	 * @return
	 * @throws Exception
	 */
	public JSONArray getMemberList(Integer projectId) throws Exception {
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.GET_MEMBERS + projectId + "/", null);
		JSONArray result = actual.getJSONArray("result");
		return result;
	}

	public JSONArray getDeployServer(String serverIdList) throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		params.put("id__in", serverIdList);
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.DEPLOY_SERVERS, params);
		return actual.getJSONArray("result");
	}

	public JSONObject getDeployService(String serviceId) throws Exception {
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.DEPLOY_SERVICE + serviceId + "/", null);
		return actual.getJSONObject("result");
	}

	public JSONObject getTaskHistory(Integer historyId, Integer taskQType) throws Exception {
		JSONObject actual = null;
		if (taskQType == DatasEnum.TaskType_Build.getValue() || taskQType == DatasEnum.TaskType_Deploy.getValue()) {
			actual = HttpClientHelperBasic.get(Constants.API.CI_TASK_HISTORY + historyId + "/", null);
		} else {
			actual = HttpClientHelperBasic.get(Constants.API.TEST_TASK_HISTORY + historyId + "/", null);
		}
		return actual.getJSONObject("result");
	}
	
	public JSONArray getTaskHistorybytaskQid(Integer taskid, Integer taskQid) throws Exception {
		    JSONObject actual = null;
			Map<String, String> params = new HashMap<String, String>();
	        params.put("TaskQueueID", taskQid.toString());
			actual = HttpClientHelperBasic.get(Constants.API.CI_TASK + taskid + "/" +"task_histories", params);
            JSONArray taskhistories = actual.getJSONObject("result").getJSONObject("all_histories").getJSONArray("results");
		return taskhistories;
	}

	public JSONObject getUser(Integer userId) throws Exception {
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.AUTH_USER + userId + "/", null);
		return actual.getJSONObject("result");
	}

	public Integer getProjectVersion(Integer projectId) throws Exception {
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.PROJECT_VERSIONS + projectId, null);
		Integer result = 0;
		try {
			result = actual.getJSONObject("result").getInt("latest_version");
		} catch (Exception ex) {
			log.error(ex.getMessage());
		}
		return result;
	}

	public void setTaskDone(JSONObject taskQueue) throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		params.put("tq_id", String.valueOf(taskQueue.getInt("id")));
		params.put("status", String.valueOf(taskQueue.getInt("Status")));
		params.put("error_msg", taskQueue.getString("ErrorMsg"));
		HttpClientHelperBasic.get(Constants.API.TQ_DONE, params);
	}

	public void setTaskdone(Integer taskqueueId,Integer status,String errormsg) throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		params.put("tq_id", taskqueueId.toString());
		params.put("status", status.toString());
		params.put("error_msg", errormsg);
		HttpClientHelperBasic.get(Constants.API.TQ_DONE, params);
	}
	public void updateTaskruntime(Integer id,String runtime,Integer BuildVersion) throws Exception {
		JSONObject params = new JSONObject();
		params.put("LastScheduleRunTime", runtime);
		params.put("BuildVersion", BuildVersion);
		JSONObject response = HttpClientHelperBasic.patchobj(Constants.API.CITASBASIC+id+"/", params);
		System.out.println(params);
		System.out.println("updateruntime"+response);
	}
	
	public JSONObject gettask_queuesbyUUID(String UUID) throws Exception {
		JSONObject params = new JSONObject();
		params.put("TaskUUID", UUID);
		JSONObject reponse = HttpClientHelperBasic.get(Constants.API.GET_AGENTTASK, params);
		return reponse;
	}
	
	public JSONObject getSectiontask_queues(Integer Tasktype , Integer SectionId , String UUID) throws Exception {
		JSONObject params = new JSONObject();
		params.put("Tasktype", Tasktype);
		params.put("SectionId", SectionId);
		params.put("TaskUUID__icontains", UUID);
		JSONObject reponse = HttpClientHelperBasic.get(Constants.API.GET_AGENTTASK, params);
		return reponse;
	}
	
	public JSONObject getSectiontask_queues(Integer Tasktype , String UUID) throws Exception {
		JSONObject params = new JSONObject();
		params.put("TaskType", Tasktype.toString());
		params.put("TaskUUID__icontains", UUID);
		JSONObject reponse = HttpClientHelperBasic.get(Constants.API.GET_AGENTTASK, params);
		return reponse;
	}
	
	public JSONArray getParameter(Integer taskId) throws Exception {
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.PARAMETER_GROUPS.replace("<task_id>", String.valueOf(taskId)), null);
		return actual.getJSONArray("result");
	}

	public String getChangeLog(Integer historyId) throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.CHANGE_LOG.replace("<history_id>", String.valueOf(historyId)), params);
		return actual.getString("result");
	}

	public void sendRTXMessage(String receiver, String content, String result) {
		HttpUnitOptions.setDefaultCharacterSet("GBK");
		String url = Constants.API.RTX;
		WebConversation wc = new WebConversation();
		WebRequest req = new PostMethodWebRequest(url);
		req.setParameter("receiver", receiver);
		req.setParameter("title", Constants.ChineseMsg.RTX_TITLE + result);
		req.setParameter("msg", content);
		try {
			wc.getResource(req);
			// WebResponse response= wc.getResource(req);
			// String resText=response.getText().replaceAll("<.*>", "").trim();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public String getParameterGroupName(String parameterId) throws Exception {
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.PARAMETER_GROUP + parameterId + "/", null);
		return actual.getJSONObject("result").getString("group_name");
	}

	public JSONArray getTaskResult(Integer taskHistoryID) throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		params.put("TaskHistoryID", taskHistoryID.toString());
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.TESTING_RESULTS, params).getJSONObject("result");
		return actual.getJSONArray("results");
	}
	
	public Integer getProjetidbytaskid(Integer taskid) throws Exception {
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.TASK_BASIC+taskid+"/",null);		
		return actual.getJSONObject("result").getInt("Project");
	}

	public JSONArray getCaseResult(Integer taskResultID, Integer Result) throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		params.put("TaskResultID", taskResultID.toString());
		params.put("Result", Result + "");
		JSONObject actual = HttpClientHelperBasic.get(Constants.API.CASE_RESULTS, params).getJSONObject("result");
		return actual.getJSONArray("results");
	}

	public JSONArray getCaseTags(String tagIDs) throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		String realTagIDs = tagIDs.substring(0, tagIDs.length() - 1);
		if (realTagIDs.contains(",")) {
			params.put("id__in", realTagIDs);
		} else {
			params.put("id", realTagIDs);
		}
		JSONArray actual = HttpClientHelperBasic.get(Constants.API.CASETAGS, params).getJSONArray("result");
		return actual;
	}

	public JSONArray getAutoCases(String caseTags, Integer projectID) throws Exception {
		Map<String, String> params = new HashMap<String, String>();
		String realTags = caseTags.substring(0, caseTags.length() - 1);
		JSONArray newResult = new JSONArray();
		params.put("ProjectID", projectID.toString());
		params.put("page_size", "10000");
		JSONArray actual = HttpClientHelperBasic.get(Constants.API.AUTOCASES, params).getJSONObject("result").getJSONArray("results");
		String[] tagArray=realTags.split(",");
		if(realTags.contains("ALL"))
		{
			newResult=actual;
		}
		else
		{
		   for(int i=0;i<tagArray.length;i++)
		   {
			   String tempTag=tagArray[i];
			   for (int j = 0; j < actual.size(); j++) {
					String tmpCaseTags = actual.getJSONObject(j).get("CaseTag").toString();
					if (tmpCaseTags.contains(tempTag))
					{
						newResult.add(actual.getJSONObject(j));
					}
				}
		   }
		}
		return newResult;
	}

}
