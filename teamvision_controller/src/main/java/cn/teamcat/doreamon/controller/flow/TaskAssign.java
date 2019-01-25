package cn.teamcat.doreamon.controller.flow;

import java.io.FileInputStream;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.Properties;

import org.apache.ibatis.session.SqlSession;
import org.apache.log4j.Logger;

import com.google.common.base.Joiner;

import cn.teamcat.doraemon.controller.db.dict.DatasEnum;
import cn.teamcat.doreamon.controller.tools.CommonUtil;
import cn.teamcat.doreamon.controller.tools.Constants;
import cn.teamcat.doreamon.controller.tools.HttpClientHelper;
import cn.teamcat.doreamon.controller.tools.HttpClientHelperBasic;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

/**
 * 任务分发
 * @author Sirui.Zhang Siyuan.Lu
 *
 */
public class TaskAssign {
	private HttpClientHelper http = new HttpClientHelper();
	private Logger log = Logger.getLogger(TaskAssign.class);
	public static CommonUtil util = new CommonUtil();
	/**
	 * 分发流程
	 * @param taskQueuelist
	 * @return
	 * @throws Exception 
	 */
	public JSONArray assign(JSONArray taskQueuelist) throws Exception{
		log.info("Controller-TaskAssign-开始运行");		
		for (int i = 0; i < taskQueuelist.size(); i++) {
			JSONObject taskQ = taskQueuelist.getJSONObject(i);
			Integer taskQStatus = taskQ.getInt("Status");
            Integer taskQid = taskQ.getInt("id");
            Integer taskType = taskQ.getInt("TaskType");
            log.info("taskQStatus"+ taskQStatus);
			//因为省略了拆分过程所以直接处理未处理任务
			if (taskQStatus == DatasEnum.TaskInQueueStatus_NoAssign.getValue()||taskQStatus == DatasEnum.TaskInQueueStatus_NoProcess.getValue()) {//选择没有分发的任务
				log.info("TaskAssign-正在处理taskQueId为"+taskQ.getInt("id")+"的任务");
				if (taskQ.getInt("Command")== DatasEnum.TQCommandType_Start.getValue() && taskType != DatasEnum.TaskType_Taskflow.getValue() && taskType != DatasEnum.TaskType_Tasksection.getValue() && taskType != DatasEnum.TaskType_Taskflow.getValue()) {//分发开始任务
					assignStartTask(taskQ);
				}else if (taskType == DatasEnum.TaskType_Taskflow.getValue() || taskType == DatasEnum.TaskType_Tasksection.getValue()) {
					assignTaskflow(taskQ);
				}else{//如果是stop任务 或者timeout任务 则直接改为以分发
					 http.setstatusstaskqueueId(taskQid, DatasEnum.TaskInQueueStatus_Assigned.getValue());
				}
			}
		}
		log.info("Controller-TaskAssign-运行完毕");
		return taskQueuelist;
	}	
	/**
	 * 分发开始任务
	 * @param taskQueueMapper
	 * @param taskQueue
	 * @param agentMapper
	 * @param result
	 * @throws Exception 
	 */
	private void assignStartTask(JSONObject taskQueue) throws Exception{
//		if (isCITask(taskQueue)) {
			try{
				Map<String,String> taskConfig = http.getCITaskConfig(taskQueue);
				if (taskConfig.get("agent_filter_type") != null) {
					if (taskConfig.get("agent_filter_type").equals("1")) {				
						JSONObject agent = http.getAgentbyid(Integer.valueOf(taskConfig.get("ci_agent_select")));						
						assignAppointAgent(taskQueue, agent);
					}else if (taskConfig.get("agent_filter_type").equals("2")){
						if (!taskConfig.get("agent_condations").equals("")) {
							JSONArray Filteragentlist = getFilterAgent(taskConfig.get("agent_condations"));
							log.info("++++Filteragentlist: "+Filteragentlist);
							for (int i = 0; i < Filteragentlist.size(); i++) {								
								JSONObject agent = Filteragentlist.getJSONObject(i);
								ArrayList<Integer> taskidlist = http.getAgentTaskid(agent.getInt("id"));
								if (!taskidlist.contains(taskQueue.getInt("TaskID"))&&isAgentFree(taskQueue , agent)) {
									assignAppointAgent(taskQueue, agent);
									break;
								}							
							}							
						}else{
							assignFreeAgent(taskQueue);
						}
					}			
				}else{
					http.updatetaskqueueErr(taskQueue.getInt("id"), Constants.ASSIGN_FAIL_FROM_INTERFACE.toString());
					throw new Exception();
				}
			}catch(Exception e){
				http.updatetaskqueuebyid(taskQueue.getInt("id"), DatasEnum.TaskInQueueStatus_Error.getValue());
				throw e;
			}
//		}else{
//			//测试任务预留
//		}
	}
	
	/**
	 * 分发Taskflow任务
	 * 
	 * @param taskQueueMapper
	 * @param taskQueue
	 * @param agentMapper
	 * @param result
	 * @throws Exception
	 */
	private void assignTaskflow(JSONObject taskQueue) throws Exception {
		log.info("进入taskflow分发处理流程");
		Integer tqid = taskQueue.getInt("id");
		String Caselist = taskQueue.getString("CaseList");
		String TaskUUID = taskQueue.getString("TaskUUID");
		Integer taskflowid = taskQueue.getInt("TaskID");
		Integer FromName = taskQueue.getInt("FromName");
		log.info("CaselistStr:" + Caselist);
		if (!Caselist.equals("null")) {
			String[] sectionidarr = Caselist.split(",");
			log.info("sectionidarr:" + sectionidarr);
			List<String> sectionidlist = Arrays.asList(sectionidarr);
			log.info("该taskflow的sectionlist为：" + sectionidlist);
			if (sectionidlist.size() > 0) {
				log.info("进入taskflow处理子section流程");
				if (Integer.valueOf(sectionidlist.get(sectionidlist.size()-1))==0) {
					http.updatetaskqueue(tqid, DatasEnum.TaskInQueueStatus_Complete.getValue(), "taskflow complete");
				}else {
					JSONObject SectionTQ = http
							.getSectiontask_queues(Integer.valueOf(DatasEnum.TaskType_Tasksection.getValue()), TaskUUID);
					if (SectionTQ.getJSONArray("result").size() == 0) {
						String TASK_FLOW_SWITCH = getProperty("TASK_FLOW_SWITCH");
						if (TASK_FLOW_SWITCH.equals("true")) {
							log.info("判断已执行的section任务状态是否成功，不成功停止TaskFlow");
							Integer failSectionnumber = getFailsection(taskflowid, TaskUUID);
							if (failSectionnumber > 0) {
								http.updatetaskqueueCaseList(tqid, "0");
							} else {
								assignSection(sectionidlist, tqid, TaskUUID,FromName);
							}
						} else {
							log.info("无正在运行section,开始下发section");
							assignSection(sectionidlist, tqid, TaskUUID,FromName);
						}
					}
				}			
			}
		}
	}
		
//	/**
//	 * 获取CI任务配置信息
//	 * @param taskQueue
//	 * @return
//	 * @throws Exception
//	 */
//	private Map<String,String> getCITaskConfig(TaskQueueMapper taskQueueMapper,TaskQueue taskQueue) throws Exception{
//		Map<String ,String> basic = new HashMap<String, String>();
//		JSONObject result = http.getTaskInfo(taskQueue.getTaskid(),taskQueue.getTasktype());
//		JSONArray parameter =result.getJSONObject("task_config").getJSONObject("basic_section").getJSONArray("plugins").getJSONObject(0).getJSONArray("parameter");
//		for (int i = 0; i < parameter.size(); i++) {
//			JSONObject obj = parameter.getJSONObject(i);
//				basic.put(obj.getString("name"), obj.getString("value"));
//		}
//		return basic;
//	}
	
	/**
	 * 下发section
	 * @param sectionidlist
	 * @param tqid
	 * @param TaskUUID
	 * @param agentId
	 * @throws Exception 
	 * @throws NumberFormatException 
	 */
	private void assignSection( List<String> sectionidlist , Integer tqid , String TaskUUID ,Integer fromname) throws NumberFormatException, Exception{
		for (int i = 0; i < sectionidlist.size(); i++) {
			if (Integer.valueOf(sectionidlist.get(i)) != 0) {
				insertSectionTaskQueue(Integer.valueOf(sectionidlist.get(i)), Integer.valueOf(DatasEnum.TaskType_Tasksection.getValue()), TaskUUID,fromname);
				sectionidlist.set(i, "0");
				String sectionidliststr = Joiner.on(",").join(sectionidlist); 
				http.updatetaskqueueCaseList(tqid , sectionidliststr);	
				break;
			}
		}
		
	}
	/**
	 * 插入section task queue
	 * @param taskId
	 * @param taskType
	 * @param TaskUUID
	 * @throws Exception 
	 * @throws NumberFormatException 
	 */
	
	public static void insertSectionTaskQueue(Integer taskId, Integer taskType,String uuid,Integer fromname)
			throws Exception {
		JSONObject params = new JSONObject();
		String taskuuid =uuid;
		params.put("TaskID", taskId);
		params.put("Status", DatasEnum.TaskInQueueStatus_NoProcess.getValue());
		params.put("TaskType", taskType);
		params.put("ParentID", "0");
		params.put("FromName", fromname);
		Date now =  util.getUTCDate();
		SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS");
	    String runtimeString = String.valueOf(simpleDateFormat.format(now));
		params.put("EnqueueTime", runtimeString+"+00:00");
		params.put("TaskUUID", taskuuid);
		params.put("Command", DatasEnum.TQCommandType_Start.getValue());
		params.put("IsLocked", false);
		params.put("Priority", 2);
		params.put("BuildParameterID", "0");
		System.out.println(params);
		JSONObject aJsonObject =HttpClientHelperBasic.postobj(Constants.API.GET_AGENTTASK, params);
		System.out.println(aJsonObject);
	}
	
	/**
	 * 获取taskflow下面已经失败的section个数
	 * @param sectionidlist
	 * @param tqid
	 * @param TaskUUID
	 * @param agentId
	 * @throws Exception 
	 * @throws NumberFormatException 
	 */
	private  Integer getFailsection( Integer taskflowid , String TaskUUID ) throws Exception{		
		JSONObject taskflowhistory = http.getCITaskFlowHistoryId(taskflowid, TaskUUID);
		if (taskflowhistory.getJSONObject("result").getJSONArray("results").size()>0) {
			Integer taskflowhistoryid = taskflowhistory.getJSONObject("result").getJSONArray("results").getJSONObject(0).getInt("id");
			JSONObject tasksectionhistory = http.getCITaskSectionHistoryIdbyStatus(taskflowhistoryid,TaskUUID,DatasEnum.TaskStatus_Completed.getValue());
			Integer tasksectionhistorysize = tasksectionhistory.getJSONObject("result").getJSONArray("results").size();
			return tasksectionhistorysize;
		}
		else {
			return 0;
		}

	}	 
	
	/**
	 * 分配给指定Agent
	 * @param taskQueueMapper
	 * @param taskQueue
	 * @param agentMapper
	 * @param agentId
	 */
	private void assignAppointAgent( JSONObject taskQueue, JSONObject agent){
		try{
			if (agent != null) {
				if (isAgentFree(taskQueue,agent)) {//
					updateStartTaskStatus(taskQueue, agent.getInt("id"));
				}else{
					log.info("TaskAssign-指定Agent不可用");
				}
			}else{
				log.info("TaskAssign-当前任务无可用Agent");
			}
		}catch(Exception e){
			
		}
		
	}
	 
	/**
	 * 分配任意空闲Agent
	 * @param taskQueueMapper
	 * @param taskQueue
	 * @param agentMapper
	 * @throws Exception 
	 */
	private void assignFreeAgent(JSONObject taskQueue) throws Exception{
		JSONArray agentList = getOnlineAgentList();
		if(agentList.size() > 0){
			for (int i = 0; i < agentList.size(); i++){
				JSONObject agent = agentList.getJSONObject(i);
				if (isAgentFree(taskQueue, agent)) {//				
					updateStartTaskStatus(taskQueue, agent.getInt("id"));
					break;
				}
			}
		}else{
			log.info("TaskAssign-当前任务无可用Agent");
		}
	}
	
	/**
	 * 判断当前Agent是否可用
	 * @param taskQueueMapper
	 * @param taskQueue
	 * @param agentMapper
	 * @param agent
	 * @return
	 * @throws Exception 
	 */
	private Boolean isAgentFree(JSONObject taskQueue, JSONObject agent) throws Exception{

		Integer agentid = agent.getInt("id");
		Integer command = taskQueue.getInt("Command");
		JSONArray taskQs = http.getTaskQbyagentid(agentid, command);
		Integer agentTasks = taskQs.size();
		System.out.println("++++++++agentTasks="+agentTasks);
		System.out.println("++++++++agent.getExecutors()="+agent.getInt("Executors"));
		JSONArray appointTasks = http.getappointTask(taskQueue.getInt("TaskType"), taskQueue.getInt("TaskID"), agentid, DatasEnum.TQCommandType_Start.getValue());
	    Integer appointTask = appointTasks.size();
		System.out.println("++++++++appointTask="+appointTask);
		System.out.println("++++++++agent.getStatus()="+agent.getInt("Status"));
		//agent 执行器未满 & 无该任务 & 在线状态
		boolean free = agentTasks < agent.getInt("Executors") && appointTask == 0 && agent.getInt("Status") == DatasEnum.AutoAgentStatus_Online.getValue();
		return free;
	}
	
	
	/**
	 * 判断任务类型
	 * @param taskQueue
	 * @return
	 **/
	private Boolean isCITask(JSONObject taskQueue){
		int taskType = taskQueue.getInt("TaskType");
		if (taskType == DatasEnum.TaskType_Build.getValue() || taskType == DatasEnum.TaskType_Deploy.getValue()) {
			return true;
		}else{
			return false;
		}
	}
	
	/**
	 * 更改Start任务状态
	 * @param taskQueueMapper
	 * @param taskQueue
	 * @param agentMapper
	 * @param agent
	 * @param agentId
	 * @throws Exception 
	 */
	private void updateStartTaskStatus( JSONObject taskQueue, Integer agentId ) throws Exception{
		Integer taskQid = taskQueue.getInt("id");
		http.setstatusagentidbytaskqueueId(taskQid, DatasEnum.TaskInQueueStatus_Assigned.getValue(), agentId);	
		if (taskQueue.getInt("TaskType")== DatasEnum.TaskType_Interface.getValue()) {
			JSONObject actual = http.getTaskResultsbyTaskUUid(taskQueue.getString("TaskUUID"));
			JSONArray testTaskResultList = actual.getJSONObject("result").getJSONArray("results");
			if (testTaskResultList.size() > 0) {
				JSONObject testTaskResult = testTaskResultList.getJSONObject(0);
				Integer testTaskResultid = testTaskResult.getInt("id");
				http.updatetaskresultbyid(testTaskResultid, agentId);
			}
		}
	}
	
	/**
	 * 获取在线的Agent列表
	 * @param session
	 * @return
	 * @throws Exception 
	 */
	private JSONArray getOnlineAgentList() throws Exception{
		JSONObject actual = http.getonlineagentlist(DatasEnum.AutoAgentStatus_Online.getValue());
		JSONArray agentList = actual.getJSONArray("result");
		return agentList;
	}

	/**
	 * 获取符合筛选条件的Agent
	 * @param session
	 * @return
	 * @throws Exception 
	 */
	private JSONArray getFilterAgent(String agentFilters) throws Exception{
		JSONObject agent = new JSONObject();
		String[] filters = agentFilters.split(",");
		JSONArray agentList = getOnlineAgentList();
		JSONArray Filteragentlist = new JSONArray();		
		if (agentList.size() > 0) {			
			for (int i = 0; i < agentList.size(); i++) {
				int f = 0;
				for (int j = 0; j < filters.length; j++) {
					if (agentList.getJSONObject(i).getString("AgentTags").contains(filters[j]))
						f = f + 1;
				}
				if (f == filters.length){
					agent = agentList.getJSONObject(i);
					Filteragentlist.add(agent);
				}
			}
		}
		return Filteragentlist;
	}

	private static String getProperty(String property){
		try {
			Properties properties = new Properties();
			FileInputStream fis = new FileInputStream("controller.properties");
			properties.load(fis);  
			return properties.getProperty(property);
		} catch (Exception e) {
			return "";
		}
	}
//	/**
//	 * 根据任务类型处理任务
//	 * @param taskQId
//	 * @param agentIdList
//	 * @param configId
//	 */
//	private void taskProcess(int taskQId,List<?> agentIdList,int configId){
//		switch (Constants.config.getTaskType(configId)) {
//		case DatasDict.AutoTaskType_APPUI:
//			log.info("TaskAssign-进入APPUI任务流程");
//			appTask(configId, taskQId);
//			break;
//		case DatasDict.AutoTaskType_Interface:
//			log.info("TaskAssign-进入Interface任务流程");
//			if (agentIdList.size()>0)			
//				interfaceTask(taskQId, agentIdList);
//			else
//				log.info("TaskAssign-当前无可用的Agent");
//			break;
//		case DatasDict.AutoTaskType_WebUI:
//			log.info("TaskAssign-进入WebUI任务流程");
//			if (agentIdList.size()>0)	
//				webTask(taskQId, agentIdList, configId);
//			else
//				log.info("TaskAssign-当前无可用的Agent");
//			break;
//		}
//	}
//	
//	/**
//	 * 父子任务流程判断
//	 * @param taskQId
//	 * @param agentIdList
//	 * @param configId
//	 * @param TQTaskUUID
//	 */
//	private void taskAssign(int taskQId,List<?> agentIdList,int configId,String TQTaskUUID){
//		if (agentIdList.size()>0) {
//			if (!Constants.taskQ.getWhetherHasChild(TQTaskUUID)) {
//				log.info("TaskAssign-进入无子任务处理流程");
//				taskProcess(taskQId, agentIdList, configId);
//			}else{
//				log.info("TaskAssign-进入子任务处理流程");
//				List<?> broTaskQList  = Constants.taskQ.addSubtaskToList(TQTaskUUID);
//				for (int j = 0; j < broTaskQList.size(); j++) {
//					int subtaskQId = Integer.valueOf(broTaskQList.get(j).toString());
//					//判断任务状态
//					if (1Constants.taskCtrl.isTaskStatus(Constants.taskQ.getTaskStatus(subtaskQId), DatasDict.TaskInQueueStatus_NoAssign)) {
//						taskProcess(subtaskQId, agentIdList, configId);
//					}
//				}
//				if (Constants.taskCtrl.isTaskListStatus(broTaskQList, DatasDict.TaskInQueueStatus_Assigned)) {
//					Constants.taskQ.updateTaskQueueStatus(taskQId, DatasDict.TaskInQueueStatus_Assigned);
//				}
//			}
//		}
//	}
//	
//	/**
//	 * 移动任务处理
//	 * @param configId
//	 * @param taskQId
//	 */
//	private void appTask(int configId,int taskQId){
//		AutotestingMobiledeviceService device = new AutotestingMobiledeviceService();
//		List<?> deviceIdList = new ArrayList<>();
//		String osV = Constants.config.getOsVsersion(configId);
//		if(!osV.equals("0")){
//			deviceIdList = device.findFreeMobile(Constants.config.getOsTpye(configId), osV);
//		}else{
//			deviceIdList = device.findFreeMobile(Constants.config.getOsTpye(configId));
//		}
//		log.info("TaskAssign-当前可用的deviceIdList："+deviceIdList);
//		if (deviceIdList.size()>0) {
//			int deviceId = Integer.valueOf(deviceIdList.get(0).toString());
//			log.info("TaskAssign-该任务使用的设备deviceId："+deviceId);
//			Constants.taskQ.updateTaskAgent(taskQId, device.getAgentId(deviceId));
//			Constants.taskQ.updateTaskDevice(taskQId, deviceId);
//			Constants.taskQ.updateTaskQueueStatus(taskQId, DatasDict.TaskInQueueStatus_Assigned);
//			device.updateDeviceStatus(deviceId, DatasDict.MobileDeviceStatus_Assigned);
//		}else{
//			log.info("TaskAssign-当前无可用设备");			
//		}
//	}
//	
//	/**
//	 * 接口任务处理
//	 * @param taskQId
//	 * @param agentIdList
//	 */
//	private void interfaceTask(int taskQId , List<?> agentIdList){
//		int agentId = Integer.valueOf(agentIdList.get(0).toString());
//		log.info("该任务使用的agentId:"+agentId);
//		Constants.taskQ.updateTaskAgent(taskQId, agentId);
//		Constants.taskQ.updateTaskQueueStatus(taskQId, DatasDict.TaskInQueueStatus_Assigned);
//		agent.updateAgentStatus(agentId, DatasDict.AutoAgentStatus_Assigned);
//	}
//	
//	
//	/**
//	 * webUI任务处理
//	 * @param taskQId
//	 * @param agentIdList
//	 * @param configId
//	 */
//	private void webTask(int taskQId , List<?> agentIdList,int configId){
//		String configBrowser = Constants.config.getBrowser(configId);
//		log.info("任务需求的浏览器类型:"+configBrowser);
//		for (int i = 0; i < agentIdList.size(); i++) {
//			int agentId = Integer.valueOf(agentIdList.get(i).toString());
//			if (agent.getBrowser(agentId).contains(configBrowser)) {//是否包含可用浏览器
//				log.info("该任务使用的agentId:"+agentId);
//				Constants.taskQ.updateTaskAgent(taskQId, agentId);
//				Constants.taskQ.updateTaskQueueStatus(taskQId, DatasDict.TaskInQueueStatus_Assigned);
//				agent.updateAgentStatus(agentId, DatasDict.AutoAgentStatus_Assigned);
//			}
//		}
//	}
//	
}
