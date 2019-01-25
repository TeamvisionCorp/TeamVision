package cn.teamcat.doreamon.controller.flow;

import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Locale;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;
import org.apache.ibatis.session.SqlSession;
import org.apache.log4j.Logger;

import cn.teamcat.doraemon.controller.db.dict.DatasEnum;
import cn.teamcat.doreamon.controller.tools.CommonUtil;
import cn.teamcat.doreamon.controller.tools.Constants;
import cn.teamcat.doreamon.controller.tools.EmailHelper;
import cn.teamcat.doreamon.controller.tools.HttpClientHelper;
import cn.teamcat.doreamon.controller.tools.SocketHelper;
import cn.teamcat.doreamon.controller.tools.TaskStatusController;

/**
 * 任务发送
 * @author Sirui.Zhang Siyuan.Lu
 *
 */
public class TaskSend {

	private Logger log = Logger.getLogger(TaskSend.class);
//	private SocketHelper socket = new SocketHelper();
	private HttpClientHelper http = new HttpClientHelper();
	/**
	 * 发送方法
	 * @param taskQueIdList
	 * @throws Exception
	 *
	 */
	public void send(JSONArray taskQueueList) throws Exception{
		log.info("Controller-TaskSend-开始运行");
		for (int i = 0; i < taskQueueList.size(); i++) {
			JSONObject taskQ = taskQueueList.getJSONObject(i);
			Integer taskQId = taskQ.getInt("id");
			 Integer taskType = taskQ.getInt("TaskType");
			if (taskQ.getInt("Status") == DatasEnum.TaskInQueueStatus_Assigned.getValue() && taskType != DatasEnum.TaskType_Taskflow.getValue() && taskType != DatasEnum.TaskType_Tasksection.getValue()) {
				log.info("Controller-TaskSend-正在处理taskQueId为"+taskQId+"的任务");
				Integer cmd = taskQ.getInt("Command");
				if (cmd == DatasEnum.TQCommandType_Start.getValue()) {
				JSONObject agent = http.getAgentbyid(taskQ.getInt("AgentID"));
				if (cmd == DatasEnum.TQCommandType_Start.getValue() && !TaskStatusController.isFinished(taskQ.getInt("Status")) && agent.getInt("Status")== DatasEnum.AutoAgentStatus_Online.getValue()){//处理开始命令
					log.info("Controller-TaskSend-进入Start任务流程");					
					int AgentID = taskQ.getInt("AgentID");
					Boolean ifSend = isTaskconflict(taskType,AgentID);
					if (ifSend == false) {
						sendStartCmd(taskQ, agent, taskQId);
						sendStartMsg();
					}
				}
				}else if(cmd == DatasEnum.TQCommandType_Stop.getValue() | cmd == DatasEnum.TQCommandType_Timeout.getValue()){//处理停止及超时命令
					log.info("Controller-TaskSend-进入Stop任务流程");
					sendStopTimeoutCmd(taskQ, taskQId);
				}
			}
		}
		log.info("Controller-TaskSend-运行完毕");
	}
	/**
	 * 判断任务是否冲突
	 * @param taskQueIdList
	 * @throws Exception 
	 * 
	 */
	public Boolean isTaskconflict(Integer tasktype,Integer AgentID) throws Exception {
		JSONObject actul = http.getrunning_testtypelist(AgentID);
		JSONArray result = actul.getJSONArray("result");
		Boolean istaskconflict;
		if (result.size()>0 && tasktype==1 ) {
			istaskconflict = true;
		}
		else {
			istaskconflict = false;
		}
		return istaskconflict;		
	}
		
	/**
	 * 判断任务是否冲突
	 * @param taskQueIdList
	 * @throws Exception 
	 * 
	 */
	public void sendStartMsg() throws Exception {
		try {
			JSONObject reponse = new JSONObject();
			reponse = HttpClientHelper.postMq("TASKSTATUSCHANGE","the task has sent");
		} catch (Exception e) {
			log.info(Constants.MQ_TIMEOUT_ERROR);
			e.printStackTrace();
		} 	
	}
	

	/**
	 * 发送命令前判断是否需要发出
	 * @param taskQMapper
	 * @param taskQ
	 * @param agentMapper
	 * @param agent
	 * @param taskQId
	 * @throws Exception 
	 */
	private void sendStopTimeoutCmd(JSONObject taskQ,Integer taskQId) throws Exception{
		//修改成uuid匹配
		JSONObject actual = http.getTaskqueuesbyuuidandCommand(taskQ.getString("TaskUUID"),DatasEnum.TQCommandType_Start.getValue());
		JSONArray startTaskQList =actual.getJSONArray("result");
		if (startTaskQList.size()>0) {
			for (int i = 0; i < startTaskQList.size(); i++) {//停止所有相同uuid的开始任务
				JSONObject startTaskQ = startTaskQList.getJSONObject(i);
				if (startTaskQ.getInt("Status") == DatasEnum.TaskInQueueStatus_Running.getValue()) {
					Integer Agentid = startTaskQ.getInt("AgentID");
					JSONObject agent = http.getAgentbyid(Agentid);
					stopTimeoutRunningTask(taskQ, startTaskQ, agent, getStopCmd(startTaskQ.getInt("id"),taskQ,0));
				}else{
					stopTimeoutNotRunTask(startTaskQ);
				}
			}
		}
		http.deleteTaskqueuebyid(taskQId);
	}	
	
	
	/**
	 * 停止运行中任务
	 * @param taskQMapper
	 * @param taskQ
	 * @param startQ
	 * @param agent
	 * @param cmd
	 * @throws Exception 
	 */
	private void stopTimeoutRunningTask(JSONObject taskQ,JSONObject startTaskQ,JSONObject agent,String cmd ) throws Exception{
		String ip = agent.getString("IP");
		Integer port = agent.getInt("AgentPort");
		log.info("AgentUrl:" + ip + " AgentPort:"+port + " CMD:" + cmd);
		JSONObject reponse = new JSONObject();
//		try {
//			reponse = socket.socket(ip, port, cmd);
//		} catch (Exception e) {
//			reponse = Constants.SOCKET_TIMEOUT_ERROR;
//			e.printStackTrace();
//		} 		
		try {
			//reponse = socket.socket(url, port, cmd);
			reponse = HttpClientHelper.postMq("CI_AGENT_"+String.valueOf(agent.getInt("id")),"\""+cmd+"\"");
		} catch (Exception e) {
			log.info(Constants.MQ_TIMEOUT_ERROR);
			e.printStackTrace();
		} 
		if (!reponse.equals(startTaskQ.getInt("id")+"")) {//发送命令
			stopTaskFail(taskQ, startTaskQ,reponse.toString());
		}
	}
	
	/**
	 * 停止未运行任务
	 * @param taskQMapper
	 * @param historyMapper
	 * @param startTaskQ
	 * @throws Exception 
	 */
	private void stopTimeoutNotRunTask(JSONObject startTaskQ) throws Exception{
		Integer TaskID = startTaskQ.getInt("TaskID");
		JSONObject actual = http.getTaskhistories(TaskID, startTaskQ.getInt("id"));
		JSONArray historyList = actual.getJSONObject("result").getJSONObject("all_histories").getJSONArray("results");
		if (historyList.size()>0) {
			JSONObject history = historyList.getJSONObject(0);
			Integer historyid = history.getInt("id");
			http.updatetaskhistoryTqid(historyid, 0);
			http.deleteTaskqueuebyid(startTaskQ.getInt("id"));
		}
	}
	
	/**
	 * 停止任务失败异常处理
	 * @param taskQueId
	 * @param startQueId
	 * @throws Exception 
	 */
	private void stopTaskFail( JSONObject taskQ,JSONObject startTaskQ,String reponse) throws Exception{
		if (!TaskStatusController.isFinished(startTaskQ.getInt("Status"))) {//如果未完成 将该任务改为异常
			if (taskQ.getInt("Command") == DatasEnum.TQCommandType_Stop.getValue()) {				
				http.updatetaskqueue(startTaskQ.getInt("id"), DatasEnum.TaskInQueueStatus_Error.getValue(), String.valueOf(DatasEnum.TaskInQueueStatus_Error.getValue()));
			}else{
				http.updatetaskqueue(startTaskQ.getInt("id"), DatasEnum.TaskInQueueStatus_Timeout.getValue(), Constants.RUN_TIMEOUT + reponse);
			}
			try {				
				http.setTaskDone(startTaskQ);
			} catch (Exception e) {
				http.updatetaskqueue(startTaskQ.getInt("id"), DatasEnum.TaskInQueueStatus_Disaster.getValue(),startTaskQ.getString("ErrorMsg")+" "+Constants.TQ_DONE_ERROR);
				throw e;
			}
		}
	}
	
	/**
	 * 发出开始任务命令
	 * @param url
	 * @param port
	 * @param taskQueId
	 * @throws IOException 
	 * @throws Exception
	 */
	private void sendStartCmd(JSONObject taskQ,JSONObject agent,Integer taskQId) throws Exception{
		String url = agent.getString("IP");
		Integer port = agent.getInt("AgentPort");
		Integer taskid =taskQ.getInt("TaskID");	
		JSONObject actual = http.getTaskhistories(taskid, taskQId);
		JSONArray history = actual.getJSONObject("result").getJSONObject("all_histories").getJSONArray("results");
		if (history.size()>0) {
			Integer historyId = history.getJSONObject(0).getInt("id");		
			String cmd = getStartCmdJson(taskQId, taskQ, historyId).toString();
		
			log.info("AgentUrl: " + url + " AgentPort: "+port + " CMD: " + cmd);
			JSONObject reponse = new JSONObject();
			
			try {
				//reponse = socket.socket(url, port, cmd);
				reponse = HttpClientHelper.postMq("CI_AGENT_"+String.valueOf(agent.getInt("id")),"\""+cmd+"\"");
			} catch (Exception e) {
				log.info(Constants.MQ_TIMEOUT_ERROR);
				e.printStackTrace();
			} 
			
			if (reponse.getJSONObject("result").getInt("delivered_count")==1) {
				//sendDeployRTX(taskMapper, taskQ, historyId);
				updateTaskStatusAndTime(taskQ, DatasEnum.TaskInQueueStatus_Running.getValue());
			}else{
				setTaskQFail(taskQ, taskQId, Constants.SEND_FAIL + reponse, DatasEnum.TaskInQueueStatus_AssignFail.getValue());
			}
		}else{
			setTaskQFail(taskQ, taskQId, Constants.HISTORY_ERROR, DatasEnum.TaskInQueueStatus_Disaster.getValue());
		}
	}
	
	private void setTaskQFail(JSONObject taskQ,Integer taskQId,String errorMsg,int Status) throws Exception{
		log.error("任务:"+taskQId+"下发失败");
		http.updatetaskqueue(taskQId, Status, errorMsg);
	}
	
	/**
	 * 发送部署RTX
	 * @param taskMapper
	 * @param taskQ
	 * @param historyId
	 */
//	private void sendDeployRTX(CITaskMapper taskMapper,TaskQueue taskQ,int historyId){
//		if (taskQ.getTasktype() == DatasEnum.TaskType_Deploy.getValue()) {
//			CITask task =  taskMapper.selectByPrimaryKey(taskQ.getTaskid());
//			String taskName = task.getTaskname();
//			int projectId = task.getProject();
//			try {
//				EmailHelper emailHelper = new EmailHelper();
//				JSONObject history = http.getTaskHistory(historyId,taskQ.getTasktype());
//				String content = taskName + "-" + history.getString("ProjectVersion")  + "-" + history.getString("BuildVersion") 
//				+Constants.ChineseMsg.DEPLOY_TASK_START + ",部署人员：" + history.getString("StartedBy")+",详情请查看："+ Constants.API.DASHBOARD + " " + new Date();
//				http.sendRTXMessage(emailHelper.getReceiverForRTX(emailHelper.getEmail(projectId)), content, Constants.ChineseMsg.DEPLOY_TASK_START);
//			} catch (Exception e) {
//				// TODO Auto-generated catch block
//				e.printStackTrace();
//			}
//		}
//	}
	
	/**
	 * 更新任务状态和时间
	 * @param historyMapper
	 * @param taskQMapper
	 * @param taskQ
	 * @param status
	 * @throws Exception 
	 */
	private void updateTaskStatusAndTime(JSONObject taskQ,Integer status) throws Exception{
		Integer Taskid = taskQ.getInt("TaskID");
		JSONObject actual = http.getTaskhistories(Taskid, taskQ.getInt("id"));
		JSONArray historyList = actual.getJSONObject("result").getJSONObject("all_histories").getJSONArray("results");
		
		Calendar calendar = Calendar.getInstance(Locale.CHINA);
        Date now = calendar.getTime(); 
		SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS");
	    String Starttime = String.valueOf(simpleDateFormat.format(now));
	    
	    
		if (historyList.size()>0) {
			JSONObject history =historyList.getJSONObject(0);
			Integer historyid = history.getInt("id");
			http.updatetaskhistorytimeagentid(historyid, Starttime, taskQ.getInt("AgentID"));			
            http.updatetaskqueuebyidtime(taskQ.getInt("id"), Starttime, status);
		}		
	}
	
	/**
	 * 获取命令
	 * @param taskQueId
	 * @param targetQuId
	 * @return
	 */
//	private String getStartCmd(TestTaskResultMapper testTaskResultMapper,int taskQueId,TaskQueue taskQ,int historyId){
//		JSONObject json = new JSONObject();
//		json.put("taskQueueId", taskQueId);
//		json.put("taskId", taskQ.getTaskid());
//		json.put("taskType", taskQ.getTasktype());
//		json.put("historyId", historyId);
//		json.put("parameterId", taskQ.getBuildparameterid());
//		if (taskQ.getTasktype() == DatasEnum.TaskType_Interface.getValue()) {
//			TestTaskResultExample example = new TestTaskResultExample();
//			example.createCriteria().andTaskuuidEqualTo(taskQ.getTaskuuid());
//			List<TestTaskResult> testTaskResultList =testTaskResultMapper.selectByExample(example);
//			if (testTaskResultList.size()>0) {				
//			json.put("testTaskResult", testTaskResultList.get(0).getId());
////			json.put("testCaseIDList", taskQ.getCaselist());
//			}
//		}
//		json.put("cmd", "start");
//		return json.toString();
//	}
	
	
	private JSONObject getStartCmdJson(Integer taskQueId,JSONObject taskQ,Integer historyId) throws Exception{
		JSONObject json = new JSONObject();
		json.put("taskQueueId", String.valueOf(taskQueId));
		json.put("taskId", String.valueOf(taskQ.getInt("TaskID")));
		json.put("taskType", String.valueOf(taskQ.getInt("TaskType")));
		json.put("historyId", String.valueOf(historyId));
		json.put("parameterId", String.valueOf(taskQ.getString("BuildParameterID")));
		if (taskQ.getInt("TaskType") == DatasEnum.TaskType_Interface.getValue()) {
			JSONObject actual = http.getTaskResultsbyTaskUUid(taskQ.getString("TaskUUID"));
			JSONArray testTaskResultList = actual.getJSONObject("result").getJSONArray("results");
			if (testTaskResultList.size()>0) {				
			json.put("testTaskResult", String.valueOf(testTaskResultList.getJSONObject(0).getInt("id")));
//			json.put("testCaseIDList", taskQ.getCaselist());
			}
		}
		json.put("cmd", "start");
		log.info("!!!"+json);
		return json;
	}
	
	
	
	private String getStopCmd(Integer taskQueId,JSONObject taskQ,Integer historyId){
		JSONObject json = new JSONObject();
		json.put("taskQueueId", taskQueId);
		json.put("taskId", taskQ.getInt("TaskID"));
		json.put("taskType", taskQ.getInt("TaskType"));
		Integer taskCmd = taskQ.getInt("Command");
		if (taskCmd == DatasEnum.TQCommandType_Stop.getValue()) {
			json.put("cmd", "stop");
		}else{
			json.put("cmd", "timeout");
		}
		return json.toString();
	}
	
//	/**
//	 * 处理Stop或Timeout任务
//	 * @param TQTaskUUID
//	 * @param taskQueId
//	 */
//	private void sendStopTimeoutCmd(int taskId,int taskQueId){		
//		int cmdStopTaskQId =  Constants.taskQ.getStartTaskQueId(taskId);
//		if (cmdStopTaskQId != 0) {
//			String startTaskUUid =Constants.taskQ.getTQTaskUUID(cmdStopTaskQId);
//			if (!Constants.taskQ.getWhetherHasChild(startTaskUUid)) {		
//				log.info("TaskSend-进入无子任务处理流程");
//				stopTimeout(cmdStopTaskQId, Constants.taskQ.getTqagentId(cmdStopTaskQId), taskQueId);
//			}else{
//				log.info("TaskSend-进入有子任务处理流程");
//				subtaskStop(startTaskUUid,cmdStopTaskQId);
//			}
//		}
//		Constants.taskQ.delectTask(taskQueId);		
//	}
//	
//	/**
//	 * 停止有子任务的
//	 * @param startTaskUUid
//	 */
//	private void subtaskStop(String startTaskUUid,int cmdStopTaskQId){
//		List<?> subtaskQList = Constants.taskQ.addSubtaskToList(startTaskUUid);
//		for (int j = 0; j < subtaskQList.size(); j++) {z
//			int subtaskQueId = Integer.valueOf(subtaskQList.get(j).toString());
//			if (Constants.taskCtrl.isFinished(Constants.taskQ.getTaskStatus(subtaskQueId)))
//				continue;
//			else
//				stopTimeout(subtaskQueId, Constants.taskQ.getTqagentId(subtaskQueId), cmdStopTaskQId);				
//		}
//	}
//	
//	/**
//	 * 处理Start任务
//	 * @param taskQueId
//	 * @param TQTaskUUID
//	 * @param taskId
//	 * @param trtaskViewScope
//	 * @param trruntimeEnv
//	 * @param trprojectVersion
//	 * @param taskQStatus
//	 */
//	private void sendStartCmd(int taskQueId,String TQTaskUUID,int taskId,int trtaskViewScope,String trruntimeEnv,
//			String trprojectVersion,int taskQStatus){
//		if (!Constants.taskQ.getWhetherHasChild(TQTaskUUID)){
//			log.info("TaskSend-进入无子任务处理流程");
//			if (taskQStatus == DatasEnum.TaskInQueueStatus_Assigned){//父任务为已分配才下发
//				int agentId = Constants.taskQ.getTqagentId(taskQueId);
//				startCmd(agentId,taskQueId);
//				Constants.taskR.addTestrunResult(taskId, result.getSubString(Constants.taskQ.getCaseList(taskQueId), ","), TQTaskUUID, 0, trtaskViewScope, trruntimeEnv, agentId, trprojectVersion, false);
//				updateTaskStatusAndTime(taskQueId, taskId);
//			}
//		}else{
//			log.info("TaskSend-进入有子任务处理流程");
//			if (!Constants.taskR.isHasResult(TQTaskUUID)) {//没有结果才会插入
//				log.info("插入父任务结果");
//				Constants.taskR.addTestrunResult(taskId, result.getSubString(Constants.taskQ.getCaseList(taskQueId), ","), TQTaskUUID, 0, trtaskViewScope, trruntimeEnv, 0, trprojectVersion, false);
//			}
//			subtaskStart(taskQueId, TQTaskUUID, taskId, trtaskViewScope, trruntimeEnv, trprojectVersion);
//			if (Constants.task.getTaskStatus(taskId)!= DatasEnum.AutoTaskStatus_InQueue) {//如果父任务状态为不在队列 将其改为在队列		
//				updateTaskStatusAndTime(taskQueId, taskId);
//			}
//		}
//	}
//
//	/**
//	 * 给子任务下发
//	 * @param taskQueId
//	 * @param TQTaskUUID
//	 */
//	private void subtaskStart(int taskQueId,String TQTaskUUID,int taskId,int trtaskViewScope,String trruntimeEnv,String trprojectVersion){
//		List<?> sunTaskQList  = Constants.taskQ.addSubtaskToList(TQTaskUUID);
//		for (int j = 0; j < sunTaskQList.size(); j++) {
//			int subtaskQueId = Integer.valueOf(sunTaskQList.get(j).toString());
//			if (Constants.taskQ.getTaskStatus(subtaskQueId) == DatasEnum.TaskInQueueStatus_Assigned) {//已分配的才会发送			
//				int agentId =  Constants.taskQ.getTqagentId(subtaskQueId);
//				startCmd(agentId, subtaskQueId);
//				log.info("TaskQueId："+subtaskQueId+"发送完成");
//				Constants.taskR.addTestrunResult(taskId, result.getSubString(Constants.taskQ.getCaseList(subtaskQueId), ","), Constants.taskQ.getTQTaskUUID(subtaskQueId),
//						Constants.taskR.getTaskrunResultID(TQTaskUUID, false), trtaskViewScope, trruntimeEnv, agentId, trprojectVersion, true);
//				Constants.taskQ.updateStartTime(subtaskQueId, new Date());
//			}
//		}
//		if (Constants.taskCtrl.isTaskListStatus(sunTaskQList,DatasEnum.TaskInQueueStatus_Running)) {//子任务全部发送成功才会更改父任务状态
//			Constants.taskQ.updateTaskQueueStatus(taskQueId, DatasEnum.TaskInQueueStatus_Running);
//		}
//	}
//	/**
//	 * 循环下发开始任务
//	 * @param taskId
//	 * @param taskQueId
//	 */
//	private void startCmd(TaskQueueMapper taskQMapper,TaskQueue taskQ,Agent agent,int taskQId){
//		String url = agent.getIp();
//		int port = agent.getAgentport();
//		log.info("AgentUrl:"+url);
//		log.info("AgentPort"+port);
//		try {
//			socketStart(url, port,taskQId);
//		} catch (Exception e) {
//			log.error(e.getMessage(), e);
//		}
//	}
//	
	
	
}
