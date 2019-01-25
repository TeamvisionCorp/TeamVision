package cn.teamcat.doreamon.controller.flow;

import java.util.Arrays;
import java.util.Date;
import java.util.List;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

import org.apache.ibatis.session.SqlSession;
import org.apache.log4j.Logger;

import com.google.gson.JsonObject;

import cn.teamcat.doraemon.controller.db.dict.DatasEnum;
import cn.teamcat.doreamon.controller.tools.CommonUtil;
import cn.teamcat.doreamon.controller.tools.Constants;
import cn.teamcat.doreamon.controller.tools.EmailHelper;
import cn.teamcat.doreamon.controller.tools.HttpClientHelper;
import cn.teamcat.doreamon.controller.tools.ReportMaker;
import cn.teamcat.doreamon.controller.tools.TaskStatusController;

/**
 *任务清理 
 * @author Sirui.Zhang Siyuan.Lu
 *
 */
public class TaskClean {
	private Logger log = Logger.getLogger(TaskClean.class);
	private static EmailHelper emailHelper = new EmailHelper();
	private static ReportMaker reportMaker = new ReportMaker();
	private  HttpClientHelper http =  new HttpClientHelper();
	/**
	 * 清理流程
	 * @return taskQueueList 任务Id的List
	 */
	public JSONArray clean(JSONArray taskQueuelist) throws Exception{
		log.info("Controller-TaskClean-开始运行");	
		for (int i = 0; i < taskQueuelist.size(); i++) { 
			JSONObject taskQ = taskQueuelist.getJSONObject(i);
			Integer taskQStatus = taskQ.getInt("Status");
			if (TaskStatusController.isFinished(taskQStatus)) {
				log.info("Controller-TaskClean- taskQueueID:" + taskQ.getInt("id") + "该任务已完成");
				Integer taskQType = taskQ.getInt("TaskType");		
				try {
					cleanTask(taskQ, taskQType);
				} catch (Exception e) {
					log.error(e.getMessage());
					log.error(e.getStackTrace());
//					Integer taskqid = taskQ.getInt("id");
//					http.updatetaskqueuebyid(taskqid, DatasEnum.TaskInQueueStatus_Disaster.getValue());
				}
				taskQueuelist.remove(i);
				i = i - 1;
			}
		}
		log.info("Controller-TaskClean-运行完毕");
		return taskQueuelist;
	}	

	/**
	 * 清理任务列表
	 * @param taskMapper
	 * @param taskQ
	 * @param taskQId
	 * @param taskQType
	 * @throws Exception
	 */
	private void cleanTask(JSONObject taskQ,Integer taskQType) throws Exception{
		log.info("进入cleantask");
		Integer taskqId = taskQ.getInt("id");
		Integer historyId = 0;
		String uuid = taskQ.getString("TaskUUID");
		try {
			if (taskQType == DatasEnum.TaskType_Interface.getValue()) {
				updateTestTaskResult(taskQ);
			}
			historyId = updateCIHistory(taskQ).getInt("id");
			if (historyId != 0) {
				sendReport(historyId, taskQ, taskqId, taskQType);
			}
			if (uuid.contains(",")) {
				taskFlowTaskClean(uuid,taskQ);
			}	
		} catch (Exception e) {
			// TODO: handle exception
		}		
		http.deleteTaskqueuebyid(taskqId);	
		taskQSectionclean(uuid);
	}
	
	/**
	 * 判断兄弟任务是否完成
	 * @param taskQ
	 * @return
	 * @throws Exception 
	 */
	private Boolean ifothertaskesfinished(String taskuuid) throws Exception{
		Boolean sectionStatus = false;
		JSONObject respones = http.getTaskqueuesbyuuidandTasktype(taskuuid);
		JSONArray result =respones.getJSONArray("result");
		if (result.size()>0) {
			sectionStatus = false;
		}else {
			sectionStatus = true;
		}
		return sectionStatus;
	}	

	/**
	 * 判断兄弟section是否完成
	 * @param taskQ
	 * @return
	 * @throws Exception 
	 */
	private Boolean ifSectionfinished(String taskuuid) throws Exception{
		Boolean sectionStatus = false;				
		JSONObject respones = http.getSectionTaskqueuesbyuuidandTasktype(taskuuid);
		JSONArray result = respones.getJSONArray("result");
		String CaselistStr = result.getJSONObject(0).getString("CaseList");
		String[] sectionidarr = CaselistStr.split(",");
		log.info("sectionidarr:"+sectionidarr);
		List<String> sectionidlist = Arrays.asList(sectionidarr);
		log.info("sectionidlist:"+sectionidlist);
		log.info("该taskflow的sectionlist为："+sectionidlist);			
		if (sectionidlist.get(sectionidlist.size()-1).equals("0")) {
			sectionStatus = true;
		}else {
			sectionStatus = false;
		}
		return sectionStatus;
	}	
	
	
	/**
	 * 任务流中任务处理流程
	 * @param taskQ
	 * @return
	 * @throws Exception 
	 */
	private void taskFlowTaskClean(String uuid , JSONObject taskQ) throws Exception{
		log.info("判断出task为section任务，准备进去更新seciton状态流程");
		String[] uuidarr = uuid.split(",");
		List<String> uuidlist = Arrays.asList(uuidarr);
		String taskuuid = uuidlist.get(0);
		Integer taskflowid = Integer.parseInt(uuidlist.get(1));
		Integer sectionid = Integer.parseInt(uuidlist.get(2));
		JSONObject taskflowhistory = http.getCITaskFlowHistoryId(taskflowid, taskuuid);
		Integer taskflowhistoryid = taskflowhistory.getJSONObject("result").getJSONArray("results").getJSONObject(0).getInt("id");
		JSONObject tasksectionhistory = http.getCITaskSectionHistoryId(taskflowhistoryid,taskuuid,sectionid);
		Integer tasksectionhistoryid = tasksectionhistory.getJSONObject("result").getJSONArray("results").getJSONObject(0).getInt("id");
		log.info("taskflowhistoryid"+taskflowhistoryid+"tasksectionhistoryid"+tasksectionhistoryid);
		Integer tasksectionStatus = tasksectionhistory.getJSONObject("result").getJSONArray("results").getJSONObject(0).getInt("Status");
		Integer taskflowStatus = taskflowhistory.getJSONObject("result").getJSONArray("results").getJSONObject(0).getInt("Status");
		if (tasksectionStatus != DatasEnum.TaskStatus_Fail.getValue() && taskflowStatus != DatasEnum.TaskStatus_Fail.getValue()) {
			http.updateCITaskFlowHistory(taskflowhistoryid, getTaskStatus(taskQ));
			http.updateCITaskSectionHistory(tasksectionhistoryid, getTaskStatus(taskQ));
			log.info("判断出task为section任务，更新section flow history完毕");
		}else {
			http.updateCITaskFlowHistory(taskflowhistoryid);
			http.updateCITaskSectionHistory(tasksectionhistoryid);
		}					
	}
	
	private void taskQSectionclean(String uuid) throws Exception {
		String[] uuidarr = uuid.split(",");
		List<String> uuidlist = Arrays.asList(uuidarr);
		String taskuuid = uuidlist.get(0);
		Integer sectiontqid = http.getTaskfloworSectionTqid(taskuuid, DatasEnum.TaskType_Tasksection.getValue());
		Integer taskflowtqid = http.getTaskfloworSectionTqid(taskuuid, DatasEnum.TaskType_Taskflow.getValue());
		log.info("sectiontqid"+sectiontqid+"taskflowtqid"+taskflowtqid);
		if (ifothertaskesfinished(taskuuid)) {
			log.info("所有任务已完毕，清理sectiontq");
			//http.deleteTaskqueuebyid(sectiontqid);
			http.updatetaskqueue(sectiontqid, DatasEnum.TaskInQueueStatus_Complete.getValue(), "section complete");
			if (ifSectionfinished(taskuuid)) {
				log.info("所有section已完毕，清理taskflow");
				//http.deleteTaskqueuebyid(taskflowtqid);
				http.updatetaskqueue(taskflowtqid, DatasEnum.TaskInQueueStatus_Complete.getValue(), "section complete");
			}
		}	
	}
		
	/**
	 * 子流程归集测试结果
	 * @param testResultMapper
	 * @param testCaseResultMapper
	 * @param taskQ
	 * @throws Exception
	 */
	private void updateTestTaskResult(JSONObject taskQ) throws Exception{
		log.info("Controller-TaskClean-归集测试任务结果");		
		String Taskuuid = taskQ.getString("TaskUUID");
		JSONObject response = http.getTaskResultsbyTaskUUid(Taskuuid);
		log.info("进入responseresponseresponse"+response);	
		JSONArray results = response.getJSONObject("result").getJSONArray("results");	
		log.info("进入resultsresultsresultsresults"+results);	
		if (results.size()>0) {
			log.info("进入resultssize>0");	
			JSONObject result = results.getJSONObject(0);
			Integer resultID = result.getInt("id");
			String ErrorMsg = taskQ.getString("ErrorMsg");
			JSONObject failresponse = http.getCaseResultsbyTaskResultID(resultID, DatasEnum.AutoCaseStatus_Fail.getValue());
			Integer fail = failresponse.getJSONObject("result").getInt("count");
			JSONObject passresponse = http.getCaseResultsbyTaskResultID(resultID, DatasEnum.AutoCaseStatus_Pass.getValue());
			Integer pass = passresponse.getJSONObject("result").getInt("count");		
			//将未运行的任务更改成放弃
			JSONObject abortedresponse = http.getCaseResultsbyTaskResultID(resultID, DatasEnum.AutoCaseStatus_Ignore.getValue());
			Integer aborted = abortedresponse.getJSONObject("result").getInt("count");	
			Integer total =fail+pass+aborted;
			JSONObject updateresponse = http.updatecaseresult(total, pass, fail, aborted, ErrorMsg, resultID);
			log.info(total+pass+ fail+ aborted+ ErrorMsg+ resultID);
			if (updateresponse.getInt("code")==200) {
				log.info("update test TaskResult success!");
			}
		}
	}
	
	/**
	 * 更新任务历史记录
	 * @param taskQMapper
	 * @param historyMapper
	 * @param taskQ
	 * @return
	 * @throws Exception
	 */
	private JSONObject updateCIHistory(JSONObject taskQ) throws Exception{
		log.info("Controller-TaskClean-更新任务历史信息");
		Integer taskqid = taskQ.getInt("id");
		Integer Taskid = taskQ.getInt("TaskID");
		Integer BuildStatus = getTaskStatus(taskQ);
		String BuildMessage = taskQ.getString("ErrorMsg");
		JSONObject taskhistoriesresponse = http.getTaskhistories(Taskid, taskqid);
		log.info("!!!!!!!!!!!!!!!!!!!!!!!!!!!taskhistoriesresponse"+taskhistoriesresponse);
		JSONArray historyList = taskhistoriesresponse.getJSONObject("result").getJSONObject("all_histories").getJSONArray("results");	
		log.info("!!!!!!!!!!!!!!!!!!!!!!!!!!!historyList"+historyList);
		JSONObject history = null;
		if (historyList.size()>0) {
			history = historyList.getJSONObject(0);
			Integer historyid = history.getInt("id");
			if (history.getString("StartTime") != null)
				http.updatetaskhistoryEndTime(historyid);
			http.updatetaskhistory(historyid, BuildStatus, 0, BuildMessage);
		}
		return history;
	}
	
	/**
	 * 获取任务状态
	 * @param taskQ
	 * @return
	 */
	private Integer getTaskStatus(JSONObject taskQ){
		int taskQStatus = taskQ.getInt("Status");
		int taskStatus = 0;
		if(taskQStatus == DatasEnum.TaskInQueueStatus_Complete.getValue()){
			taskStatus = DatasEnum.TaskStatus_Completed.getValue();
		}else if (taskQStatus == DatasEnum.TaskInQueueStatus_Aborted.getValue()) {
			taskStatus = DatasEnum.TaskStatus_Aborted.getValue();
		}else{
			taskStatus = DatasEnum.TaskStatus_Fail.getValue();
		}
		return taskStatus;
	}
	
	
	/**
	 * 发送CI任务邮件
	 * @param taskQMapper
	 * @param taskMapper
	 * @param proMapper
	 * @param testTaskResultMapper
	 * @param testCaseResultMapper
	 * @param ciHistory
	 * @param taskQ
	 * @param taskQId
	 * @param taskQType
	 * @throws Exception
	 */
	private void sendReport(Integer historyId,JSONObject taskQ,Integer taskQId,Integer taskQType) throws Exception{
		log.info("Controller-TaskClean-开始发送CI任务邮件");
		JSONObject taskresponse = http.getCItask(taskQ.getInt("TaskID"));
        JSONObject taskresult = taskresponse.getJSONObject("result");
		String taskName = taskresult.getString("TaskName");
		Integer projectId = taskresult.getInt("Project");
		log.info(taskresponse);
		log.info(taskresult+taskName+projectId);
		log.info("start gethistory");
 		JSONObject history = http.getTaskHistory(historyId,taskQType);
		log.info("end gethistory");
		String report = reportMaker.getCIReport(history, projectId, taskQId, taskName);
		log.info("reportreportreport"+report);
		if (!report.equals("")) {
			log.info("Controller-TaskClean-正在发送TaskQueueId为" + taskQId + "的邮件");
			report = setReportSummary(taskQ, report, taskQType, taskresult, history);
			String result = getResultMsg(history,taskQ.getInt("TaskType"));
			String subject = "[" + taskName + "-" + history.getString("ProjectVersion")  + "-" + history.getString("BuildVersion") + "]"+result;
			report = report.replace("$Subject", subject);
			String receiver = emailHelper.sendEmailReport(projectId, subject, report,reportMaker.getQRCode(history));
			log.info("result"+result+"subject"+subject+"receiver"+receiver);
//			http.sendRTXMessage(receiver, subject+Constants.ChineseMsg.RTX_MSG + " " + new Date(), result);
		}else{
			log.info("Controller-TaskClean-TaskQueueId为" + taskQId + "的邮件发送失败");
		}
	}
	
	
	private String getResultMsg(JSONObject history,int taskType){
		if (taskType == DatasEnum.TaskType_Deploy.getValue()) {
			return getDeployResult(history);
		}else  if(taskType == DatasEnum.TaskType_Build.getValue()) {
			return getBuildResult(history);
		}else{
			return getAutoTestResult(history);
		}
	}
	
	
	private String getBuildResult(JSONObject history){
		String result = "";
		switch (history.getInt("BuildStatus")) {
		case 1:
			result = Constants.ChineseMsg.TASK_COMPLETE;
			break;
		case 2:
			result = Constants.ChineseMsg.TASK_FAIL;
			break;
		case 3:
			result = Constants.ChineseMsg.TASK_ABORTED;
			break;
		}
		return result;
	}
	
	private String getDeployResult(JSONObject history){
		String result = "";
		switch (history.getInt("BuildStatus")) {
		case 1:
			result = Constants.ChineseMsg.DEPLOY_TASK_COMPLETE;
			break;
		case 2:
			result = Constants.ChineseMsg.DEPLOY_TASK_FAIL;
			break;
		case 3:
			result = Constants.ChineseMsg.DEPLOY_TASK_ABORTED;
			break;
		}
		return result;
	}

	private String getAutoTestResult(JSONObject history){
		String result = "";
		switch (history.getInt("BuildStatus")) {
		case 1:
			result = Constants.ChineseMsg.AUTO_TEST_TASK_COMPLETE;
			break;
		case 2:
			result = Constants.ChineseMsg.AUTO_TEST_TASK_FAIL;
			break;
		case 3:
			result = Constants.ChineseMsg.AUTO_TEST_TASK_ABORTED;
			break;
		}
		return result;
	}
	
	/**
	 * 
	 * @param testTaskResultMapper
	 * @param testCaseResultMapper
	 * @param taskQ
	 * @param report
	 * @param taskQType
	 * @param task
	 * @param history
	 * @return
	 * @throws Exception
	 */
	private String setReportSummary(JSONObject taskQ,String report,Integer taskQType,JSONObject task,JSONObject history) throws Exception{
		if (taskQ.getInt("Status") == DatasEnum.TaskInQueueStatus_Complete.getValue()) {	
			if (taskQType == DatasEnum.TaskType_Build.getValue()) {
				report =  reportMaker.getBuildSummary(history,report);
			}else if(taskQType == DatasEnum.TaskType_Deploy.getValue()){
				report =  reportMaker.getDeploySummary(history,task,report);
			}else if(taskQType == DatasEnum.TaskType_Interface.getValue()){
				report =  reportMaker.getTestSummary(history, task, report);
			}
		}else{
			report = reportMaker.getCIFailureSummary(history,report);
		}
		return report;
	}

//	/**
//	 * 任务清理
//	 * @param remove
//	 * @param taskQueId
//	 * @param TQTaskUUID
//	 * @param taskId
//	 * @param taskQStatus
//	 * @param i
//	 * @throws Exception 
//	 */
//	private void taskClean(List<Integer> remove,int taskQueId,String TQTaskUUID,int taskId,int taskQStatus,int i){
//		log.info("TaskClean-正在处理TaskQueId为"+taskQueId+"的任务");
//		int taskRunId = 0;
//		if (!Constants.taskQ.getWhetherHasChild(TQTaskUUID)) {
//			log.info("TaskClean-进入无子任务处理流程");
//			mainTestTaskClean(taskQueId, taskQStatus, taskId, taskRunId, TQTaskUUID, remove, i);
//		}else{
//			log.info("TaskClean-进入有子任务处理流程");
//			subtaskClean(taskQueId, taskQStatus, taskId, taskRunId, TQTaskUUID, remove, taskRunId);
//		}	
//	}
//	
//	/**
//	 * 测试无子任务处理
//	 * @param taskQueId
//	 * @param taskQStatus
//	 * @param taskId
//	 * @param taskRunId
//	 * @param TQTaskUUID
//	 * @param remove
//	 * @param i
//	 * @throws Exception 
//	 */
//	private void mainTestTaskClean(int taskQueId,int taskQStatus, int taskId ,int taskRunId ,String TQTaskUUID ,List<Integer> remove, int i){		
//		if (Constants.taskCtrl.isFinished(taskQStatus)) {
//			log.info("TaskClean-该任务已完成");
//			taskRunId = result.collect(taskId, taskQueId, TQTaskUUID);
//			emailAndDelete(taskRunId, TQTaskUUID, taskId, taskQStatus, taskQueId);
//			remove.add(i);
//		}else{
//			log.info("TaskClean-该任务未完成");
//		}
//	}
//	
//	/**
//	 * 测试有子任务处理
//	 * @param taskQueId
//	 * @param taskQStatus
//	 * @param taskId
//	 * @param taskRunId
//	 * @param TQTaskUUID
//	 * @param remove
//	 * @param i
//	 * @throws Exception 
//	 */
//	private void subtaskClean(int taskQueId,int taskQStatus, int taskId ,int taskRunId ,String TQTaskUUID ,List<Integer> remove, int i){
//		List<TaskQueue> broTaskQList  = Constants.taskQ.addSubtaskToList(TQTaskUUID);
//		if (Constants.taskCtrl.isBrotherFinished(broTaskQList)) {
//			log.info("TaskClean-该任务的子任务已经全部完成");
//			int TaskStatus = brotherTask(broTaskQList, taskId);//归集子任务状态 
//			Constants.taskQ.updateTaskQueueStatus(taskQueId, TaskStatus);//并修改父任务状态
//			taskRunId = result.parentCollect(taskQueId, taskId, TQTaskUUID, TaskStatus);
//			emailAndDelete(taskRunId, TQTaskUUID, taskId, taskQStatus,taskQueId);
//			remove.add(i);
//		}else{
//			log.info("TaskClean-该任务的子任务并未全部完成");
//		}
//	}
//	
//	/**
//	 * Email发送 task删除
//	 * @param taskRunId
//	 * @param TQTaskUUID
//	 * @param taskId
//	 * @param taskQStatus
//	 * @param taskQueId
//	 * @throws Exception 
//	 */
//	private void emailAndDelete(int taskRunId,String TQTaskUUID,int taskId,int taskQStatus,int taskQueId){
//		ReportMaker reportM = new ReportMaker();
//		EmailHelper emailH = new EmailHelper();
//		String subject = "自动化测试任务["+Constants.task.getTaskName(taskId)+"]已完成";
//		if (Constants.taskQ.getCmd(taskQueId) == DatasDict.TQCommandType_RerunCase) {
//			subject = subject+"-测试结果ID："+Constants.taskQ.getReportId(taskQueId)+"失败任务重跑-";
//		}
//		int versionId = Constants.config.getTCFProjectVersion(Constants.task.getTaskConfigId(taskId));
//		String report = reportM.getReport(taskId, taskRunId, TQTaskUUID, subject);
//		try {
//			if (!emailH.sendEmailReport(versionId, subject, report)) {
//				emailH.sendEmailReport(versionId, subject, report);
//			}
//		} catch (Exception e) {
//			log.error("TaskClean-邮件发送失败");
//			e.printStackTrace();
//		}
//		Constants.taskCtrl.deleteTaskAndUpdateStatus(TQTaskUUID, taskQueId,taskId);
//	}
//	
//	/**
//	 * 处理兄弟任务并合并
//	 * @param broTaskQList
//	 * @param taskId
//	 * @return 返回子任务状态的最大值
//	 */
//	private Integer brotherTask(List<TaskQueue> broTaskQList,int taskId){
//		List<Integer> status = new ArrayList<Integer>();	
//		for (int j = 0; j < broTaskQList.size(); j++) {
//				int broTaskQueId = Integer.valueOf(broTaskQList.get(j).toString());
//				int broStatus = Constants.taskQ.getTaskStatus(broTaskQueId);
//				log.info("TaskClean-该任务的子任务"+broTaskQueId+"的任务状态为"+broStatus);
//				status.add(broStatus);
//				result.collect(taskId, broTaskQueId, Constants.taskQ.getTQTaskUUID(broTaskQueId));				
//			}
//		return Collections.max(status);
//	}
	
}
