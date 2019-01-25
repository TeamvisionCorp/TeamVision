package cn.teamcat.doreamon.controller.flow;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Locale;
import java.util.UUID;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.ibatis.session.SqlSession;
import org.apache.log4j.Logger;

import cn.teamcat.doraemon.controller.db.dict.DatasEnum;
import cn.teamcat.doreamon.controller.config.TimeoutConfig;
import cn.teamcat.doreamon.controller.tools.CommonUtil;
import cn.teamcat.doreamon.controller.tools.Constants;
import cn.teamcat.doreamon.controller.tools.HttpClientHelper;
import cn.teamcat.doreamon.controller.tools.HttpClientHelperBasic;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

/**
 * 超时处理
 * @author Sirui.Zhang Siyuan.Lu
 *
 */
public class TaskTimeout {
	private Logger log = Logger.getLogger(TaskTimeout.class);
    HttpClientHelper http = new HttpClientHelper();
	/**
	 * 超时处理
	 * @return 返回任务队列
	 * @throws Exception 
	 */	
	public JSONArray checkTimeout(JSONArray taskQueueList) throws Exception{
		log.info("Controller-TaskTimeout-开始运行");
//		lockTaskQueue(taskQMapper, taskQueueList);
		for (int i = 0; i < taskQueueList.size(); i++) {
			JSONObject taskQ = taskQueueList.getJSONObject(i);
			Integer taskQId = taskQ.getInt("id");
			
			String taskQTimestr = taskQ.getString("EnqueueTime");
			String taskQTimestrformate = taskQTimestr.substring(0, 19)+".000 CST";
			
//			String taskQTimestrregular = getLastScheduletime(taskQTimestr);			
//			taskQTimestr = taskQTimestrregular+" CST";					
//			System.out.println(taskQTimestr);			
			SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS Z");
						
			Date d = format.parse(taskQTimestrformate);
			long taskQTime =  d.getTime();			
			Integer taskQStatus = taskQ.getInt("Status");		
			if (isTimeout(taskQTime) && taskQStatus != DatasEnum.TaskInQueueStatus_Timeout.getValue()) {
				log.info("Controller-TaskTimeout-正在处理taskQueId为"+taskQId+"的任务,该任务超时");
				log.info("任务入列时间:"+taskQTime);
				if(taskQ.getInt("Command") != DatasEnum.TQCommandType_Start.getValue()){
					log.info("该任务为停止任务 已将该任务删除");
					http.deletetask(taskQId);
				}else{
					processTimeoutTask(taskQId,taskQ,taskQStatus);
				}
			}
		}
		log.info("Controller-TaskTimeout-运行完毕");
		return taskQueueList;
	}
	//正则表达式取EnqueueTime，期望取出来的结果为：2018-09-07T17:20:27
	public static String getLastScheduletime(String LastScheduleRunTime) {		
	     String regex = "[\\d\\d\\d\\d\\-\\d\\d\\-\\d\\d\\w\\d\\d\\:\\d\\d\\:\\d\\d]{19}";
	     Pattern p = Pattern.compile(regex);
	     Matcher m = p.matcher(LastScheduleRunTime);
	     // 循环，如果匹配正则，则打印输出
	     while (m.find()) {
	     System.out.println(m.group());
	     }
		 return m.group();
	     }
	
	/**
	 * 处理超时
	 * @param taskQMapper
	 * @param taskQ
	 * @param taskQStatus
	 * @throws Exception 
	 */
	private void processTimeoutTask(Integer taskQId,JSONObject taskQ,Integer taskQStatus) throws Exception{
		if(taskQStatus == DatasEnum.TaskInQueueStatus_Running.getValue() ){
			log.info("Controller-TaskTimeout-进入运行超时流程");
			runningTimeout(taskQ);
		}else if(taskQStatus == DatasEnum.TaskInQueueStatus_NoProcess.getValue() || taskQStatus == DatasEnum.TaskInQueueStatus_NoAssign.getValue() || taskQStatus == DatasEnum.TaskInQueueStatus_Assigned.getValue()) {
			log.info("Controller-TaskTimeout-进入分配超时流程");
			try {
				http.updatetaskqueue(taskQId, DatasEnum.TaskInQueueStatus_Timeout.getValue(), Constants.WAIT_TIMEOUT);
			} catch (Exception e) {
				// TODO: handle exception
			}

		}
	}
	/**
	 * 处理运行超时任务
	 * @param taskQMapper
	 * @param taskQ
	 * @throws Exception 
	 */
	private void runningTimeout(JSONObject taskQ) throws Exception{
		String taskUUID = taskQ.getString("TaskUUID");
		Integer taskId = taskQ.getInt("id");
		Integer agentId = taskQ.getInt("AgentID");
		JSONObject respones = http.gettaskqueuesbyid(taskId, DatasEnum.TQCommandType_Stop.getValue(), taskUUID);
		JSONArray result = respones.getJSONArray("result");		
		if (result.size() == 0) {
			JSONObject respones2 = http.gettaskqueuesbyid(taskId, DatasEnum.TQCommandType_Timeout.getValue(), taskUUID);
			JSONArray result2 = respones2.getJSONArray("result");
			if (result2.size() == 0)
				insertTimeoutTaskQueue(agentId, taskId, taskUUID);
		}
	}
	
	/**
	 * 插入超时命令
	 * 
	 * @param taskQMapper
	 * @param agentId
	 * @param taskId
	 * @param taskUUID
	 * @return
	 */	
	private JSONObject insertTimeoutTaskQueue(Integer agentId,Integer taskId ,String taskUUID)throws Exception {
		JSONObject params = new JSONObject();
		params.put("TaskID", taskId);
		params.put("Status", DatasEnum.TaskInQueueStatus_NoProcess.getValue());
		Date now =  new Date();
		SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS");
	    String runtimeString = String.valueOf(simpleDateFormat.format(now));
		params.put("EnqueueTime", runtimeString);		
		params.put("TaskUUID", taskUUID);	
		params.put("Command", DatasEnum.TQCommandType_Timeout.getValue());
		params.put("IsLocked", false);
		params.put("AgentID", agentId);
		params.put("Priority", 7);		
		System.out.println(params);
		JSONObject aJsonObject =HttpClientHelperBasic.postobj(Constants.API.GET_AGENTTASK, params);
		System.out.println(aJsonObject);
		JSONObject result = aJsonObject.getJSONObject("result");
		return result;
	}
	
	/**
	 * 判断是否timeout
	 * @param queueTime
	 * @return
	 */
	private boolean isTimeout(long taskQTime){
		TimeoutConfig timeout = new TimeoutConfig();
		Calendar calendar = Calendar.getInstance(Locale.CHINA);
        Date nowdate = calendar.getTime(); 
		long  time = nowdate.getTime() - taskQTime;
		if (time>timeout.getTaskWaitTimeout() || time>timeout.getTaskRunTimeout()) {
			return true;
		}else{
			return false;
		}
	}
	
	/**
	 * 将队列中任务锁定
	 * @param taskQMapper
	 * @param taskQList
	 */
	public  JSONObject locktask(Integer id)  throws Exception {
		JSONObject jsonObj = new JSONObject();
        jsonObj.put("IsLocked", "true");
		Calendar calendar = Calendar.getInstance(Locale.CHINA);
        Date now = calendar.getTime(); 
		SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS");
	    String runtimeString = String.valueOf(simpleDateFormat.format(now));
	    jsonObj.put("LockTime", runtimeString+"+00:00");
		JSONObject actual = HttpClientHelperBasic.patchobj(Constants.API.PATCH_TASKQUEUE+"/"+id, jsonObj);
		return actual;
	}
	}

