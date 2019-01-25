package cn.teamcat.doreamon.controller.flow;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import net.sf.json.JSON;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

import org.apache.commons.collections.map.StaticBucketMap;
import org.apache.ibatis.session.SqlSession;
import org.apache.log4j.Logger;

import cn.teamcat.doraemon.controller.db.dict.DatasEnum;
import cn.teamcat.doreamon.controller.tools.CommonUtil;
import cn.teamcat.doreamon.controller.tools.Constants;
import cn.teamcat.doreamon.controller.tools.EmailHelper;
import cn.teamcat.doreamon.controller.tools.HttpClientHelper;
import cn.teamcat.doreamon.controller.tools.HttpClientHelperBasic;
import cn.teamcat.doreamon.controller.tools.TaskConfig;
import cn.teamcat.doreamon.controller.tools.TaskStep;

///**
// * 任务拆分
// * @author Sirui.Zhang Siyuan.Lu
// *
// */
public class TaskSplit {
	private Logger log = Logger.getLogger(TaskSplit.class);
	private HttpClientHelper http = new HttpClientHelper();
	public static CommonUtil util = new CommonUtil();
	
	public JSONArray split(JSONArray taskQueuelist) throws Exception{
		log.info("Controller-TaskSplit-开始运行");
		HttpClientHelper http = new HttpClientHelper();
		for (int i = 0; i < taskQueuelist.size(); i++) {
			JSONObject taskQ = taskQueuelist.getJSONObject(i);
			if (taskQ.getInt("Status") == DatasEnum.TaskInQueueStatus_NoProcess.getValue() && taskQ.getInt("Command") == DatasEnum.TQCommandType_Start.getValue()) {
				Integer taskType = taskQ.getInt("TaskType");				
				Integer historyID = getHistoryID(taskQ);
				log.info("Controller-TaskSplit-正在处理taskQId为" + taskQ.getInt("id")+ "的任务");
				
				if (taskType == DatasEnum.TaskType_Interface.getValue() || taskType == DatasEnum.TaskType_WebUI.getValue() || taskType == DatasEnum.TaskType_APPUI.getValue()) {
					if (isSplited(taskQ)) {
						//分割处理流程
					}else{
						testCaseNotSplit(taskQ, historyID);
					}
				}else if (taskType == DatasEnum.TaskType_Taskflow.getValue()) {
					   //Task flow处理流程
					    taskFlowsplit(taskQ);
									
				}else if (taskType == DatasEnum.TaskType_Tasksection.getValue()) {
					   //Task section处理流程
					    taskSectionsplit(taskQ);
				}
				else {
					http.updatetaskqueueStatus(taskQ.getInt("id"), DatasEnum.TaskInQueueStatus_NoAssign.getValue());
				}
			}
		log.info("Controller-TaskSplit-运行完毕");
		}
		return taskQueuelist;
	}
	
	private void taskFlowsplit (JSONObject taskQueue) throws Exception{
		 Integer taskflowid = taskQueue.getInt("TaskID");
		 Integer tqid = taskQueue.getInt("id");
		 String SectionList = "";
		 JSONObject SectionRsp = http.getTaskflowSections(taskflowid);
		 JSONArray results = SectionRsp.getJSONObject("result").getJSONArray("results");
		 if (results.size() == 0) {
			 http.updatetaskqueue(tqid, DatasEnum.TaskInQueueStatus_Complete.getValue(), "taskFlow has no section");
		 }else {
			 for (int i = 0; i < results.size()-1; i++) {
					Integer Secitonid = results.getJSONObject(i).getInt("id");
					SectionList = SectionList + Secitonid.toString()+",";
				 }
				    SectionList = SectionList + results.getJSONObject(results.size()-1).getInt("id");
				 log.info("taskflow"+taskflowid+"包含的sectionList为:"+SectionList);
				 http.updatetaskqueueCaseList(tqid , SectionList);
				 http.updatetaskqueue(tqid, DatasEnum.TaskInQueueStatus_NoAssign.getValue(), "taskFlow has assigned");
		}
	}
	
	private void taskSectionsplit (JSONObject taskQueue) throws Exception{
		 Integer SectionId = taskQueue.getInt("TaskID");
		 Integer taskQid = taskQueue.getInt("id");
		 JSONObject SectionTasksRsp = http.getsectionTasks(SectionId);
		 String sectionUUid = taskQueue.getString("TaskUUID");
		 Integer taskflowid = SectionTasksRsp.getJSONObject("result").getInt("TaskFlow");
	     JSONArray Tasklist = SectionTasksRsp.getJSONObject("result").getJSONArray("CITaskIDs");
	     Integer fromname = taskQueue.getInt("FromName");
	     log.info("当前section"+SectionId+"有"+Tasklist.size()+"个任务需要运行，分别为"+Tasklist);
	     JSONObject taskflowhistory = http.getCITaskFlowHistoryId(taskflowid,sectionUUid);
	     if (taskflowhistory.getJSONObject("result").getJSONArray("results").size()==0) {
			 Integer taskFlowhistoryId = http.insertCITaskFlowHistory(taskflowid, taskQueue,fromname);	
			 log.info("taskFlowhistoryId"+taskFlowhistoryId+"已插入成功");
		 }  
	     Integer taskFlowhistoryId = http.getCITaskFlowHistoryId(taskflowid,sectionUUid).getJSONObject("result").getJSONArray("results").getJSONObject(0).getInt("id");
		 Integer taskFlowSectionHistoryId = http.insertCITaskSectionHistory(taskFlowhistoryId,taskflowid,SectionId,taskQueue,fromname);
		 log.info("Tasklist.size()"+Tasklist.size());
	     if (Tasklist.size()>0) {
	    	 for (int i = 0; i < Tasklist.size(); i++) {
		    	 JSONObject taskbasicRsp = http.getci_tasklistbytaskid(Tasklist.getInt(i));
		    	 JSONObject task = taskbasicRsp.getJSONObject("result");
		 		 Integer taskId = task.getInt("id");
				 Integer taskType = task.getInt("TaskType");
				 Integer BuildVersion = task.getInt("BuildVersion");
				 String TaskName = task.getString("TaskName");
				 log.info("!" + taskId + "!" + taskType + "!" + BuildVersion + "!" + TaskName);
				 log.info("taskId:" + taskId + " 因所在section"+SectionId+"启动，开始入列流程");
				 SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS");
				 String runtimeString = String.valueOf(simpleDateFormat.format(util.getUTCDate()));
				 http.updateTaskruntime(taskId, runtimeString,BuildVersion+1);
				 String buildparameterid = Timer.setBuildParameterid(taskId);
				 JSONObject taskQ = insertTaskQueue(taskId, taskType, buildparameterid,taskQid,taskflowid,SectionId,sectionUUid,fromname);
				 log.info("插入taskqueues成功");
				 Integer taskhistoryId = insertCITaskHistory(taskQ, task, taskId, buildparameterid,taskFlowSectionHistoryId);
				 Timer.updateCITasklastHistory(taskId, taskhistoryId);	    	 
			}
		} 
	    http.updatetaskqueue(taskQid, DatasEnum.TaskInQueueStatus_Running.getValue(), "taskSection start");	
	    if (Tasklist.size()==0) {
	    	 http.updatetaskqueue(taskQid, DatasEnum.TaskInQueueStatus_Complete.getValue(), "taskSection has no tasks");
		}
	    log.info("更新section Status成功！");
	}
	
	public static JSONObject insertTaskQueue(Integer taskId, Integer taskType, String buildparameterid,Integer ParentID,Integer taskflowid,Integer SectionId,String uuid,Integer fromname)
			throws Exception {
		JSONObject params = new JSONObject();
		String taskuuid =uuid+","+taskflowid+","+SectionId;
		params.put("TaskID", taskId);
		params.put("Status", DatasEnum.TaskInQueueStatus_NoProcess.getValue());
		params.put("TaskType", taskType);
		params.put("ParentID", ParentID);
		params.put("FromName", fromname);
		Date now =  util.getUTCDate();
		SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS");
	    String runtimeString = String.valueOf(simpleDateFormat.format(now));
		params.put("EnqueueTime", runtimeString+"+00:00");
		params.put("TaskUUID", taskuuid);
		params.put("Command", DatasEnum.TQCommandType_Start.getValue());
		params.put("IsLocked", false);
		params.put("Priority", 2);
		if (!buildparameterid.equals("")) {
		params.put("BuildParameterID", buildparameterid);
		}
		System.out.println(params);
		JSONObject aJsonObject =HttpClientHelperBasic.postobj(Constants.API.GET_AGENTTASK, params);
		System.out.println(aJsonObject);
		JSONObject result = aJsonObject.getJSONObject("result");
		return result;
	}
	
	public Integer insertCITaskHistory(JSONObject taskQ, JSONObject task, Integer taskId,
			String buildparameterid,Integer taskFlowSectionHistoryId) throws Exception {
		Integer taskhistoryid = null;
		try {
			JSONObject params = new JSONObject();
			params.put("BuildStatus", 0);
			params.put("BuildLog", 0);
			params.put("FlowSectionHistory", taskFlowSectionHistoryId);
			params.put("TaskQueueID", taskQ.getInt("id"));
			params.put("TaskUUID", taskQ.getString("TaskUUID"));
			params.put("Command", DatasEnum.TQCommandType_Start.getValue());
			params.put("IsLocked", false);
			params.put("Priority", 2);
			int buildVersion = task.getInt("BuildVersion")+1;
			if (buildVersion == 0)
				buildVersion = 1;
			params.put("ProjectVersion", http.getProjectVersion(task.getInt("Project")));
			params.put("BuildVersion", buildVersion);
			params.put("StartedBy", 0);
			params.put("CITaskID", taskId);
			if (!buildparameterid.equals(""))
				params.put("buildparameterid", 2);
			JSONObject response = HttpClientHelperBasic.postobj(Constants.API.CITASK + taskId + "/task_histories/",
					params);
			taskhistoryid = response.getJSONObject("result").getJSONObject("all_histories").getInt("id");
			log.info("插入taskhistroy成功");
		} catch (Exception e) {
			log.info(e.getMessage());
			log.error(e.getMessage());
			EmailHelper email = new EmailHelper();
			email.sendErrorMail(task);
		}
		return taskhistoryid;
	}
	
	/**
	 * 判断是否有分割
	 * @param taskQueueMapper
	 * @param taskQueue
	 * @return
	 * @throws Exception
	 */
	private boolean isSplited(JSONObject taskQueue) throws Exception{
		boolean isSplited = false;
		Map<String,String> taskConfig = http.getCITaskConfig(taskQueue);
		if (taskConfig.get("agent_filter_type") != null) {
			if (!taskConfig.get("agent_filter_type").equals("2")){
				isSplited = true;
			}			
		}else{
			isSplited = false;
		}
		if (taskConfig.get("is_splited") != null) {
			if (taskConfig.get("is_splited").equals("1")){
				isSplited = true;
			}		
		}else{
			isSplited = false;
		}
		if (taskQueue.getInt("TaskType") != DatasEnum.TaskType_Interface.getValue()){
			isSplited = true;
		}else{
			isSplited = false;
		}
		return isSplited;
	}
	
	
	
	/**
	 * 分配测试用例不拆分
	 * @param taskQueueMapper
	 * @param testCaseMapper
	 * @param taskQueue
	 * @throws Exception 
	 */
	
	
//	private void testCaseNotSplit (CITaskMapper taskMapper,TaskQueueMapper taskQueueMapper,TestCaseMapper testCaseMapper,TestTaskResultMapper testTaskResultMapper,TestCaseResultMapper testCaseResultMapper,TaskQueue taskQueue, int historyId) throws Exception{
//		String caseIdList ="";
//		JSONArray testCaseList=this.getTestCaseList(taskMapper, taskQueueMapper, taskQueue);
//		int total = testCaseList.size();
//		if (total > 0) {
//			for (int i = 0; i < total; i++) {
//				caseIdList = caseIdList + testCaseList.getJSONObject(i).getString("id")+ ",";
//			}
//		} 
//		taskQueue.setCaselist(caseIdList);
//		log.info("Controller-TaskSplit-该任务caseIdList："+caseIdList);
//		taskQueue.setStatus(DatasEnum.TaskInQueueStatus_NoAssign.getValue());
//		taskQueueMapper.updateByPrimaryKey(taskQueue);
//		TestTaskResult taskResult = inertTestTaskResult(testTaskResultMapper, taskQueue, historyId, total, 0);
//	    insertTestCaseResult(testCaseResultMapper, testCaseList, taskResult);
//	}
	
	
	private void testCaseNotSplit (JSONObject taskQueue, Integer historyId) throws Exception{
		Integer taskQid = taskQueue.getInt("id");
		http.updatetaskqueueStatus(taskQid, DatasEnum.TaskInQueueStatus_NoAssign.getValue());			
		inertTestTaskResult(taskQueue, historyId, 0, 0);

	}
	
	
	
	private JSONArray  getTestCaseList(JSONObject taskQueue) throws Exception
	{
		Map<String,String> ciTaskConfig=http.getCITaskConfig(taskQueue);
		String caseFilter="";
		if( ciTaskConfig.containsKey("autocase_filter"))
		{
			caseFilter=ciTaskConfig.get("autocase_filter");
		}
		JSONArray caseArray=null;
		JSONArray caseTagArray=null;
		String caseTags="";
		if(caseFilter=="" || caseFilter=="1,")
		{
			caseTagArray=http.getCaseTags("1,");
		}
		else
		{
			caseTagArray=http.getCaseTags(caseFilter);
		}
		for(int i=0;i<caseTagArray.size();i++)
		{
			caseTags=caseTags+caseTagArray.getJSONObject(i).getString("TagName")+",";
		}
		Integer Taskid = taskQueue.getInt("TaskID");
		Integer Projectid = http.getProjetidbytaskid(Taskid);
		caseArray=http.getAutoCases(caseTags,Projectid);
		return caseArray;
	}

	
	private int getHistoryID(JSONObject taskQ) throws Exception{
		Integer taskid = taskQ.getInt("TaskID");
		Integer taskQid = taskQ.getInt("id");
		JSONArray historylist = http.getTaskHistorybytaskQid(taskid, taskQid);		
		int historyId = 0;
		if (historylist.size() > 0) {
			historyId = historylist.getJSONObject(0).getInt("id");
		}
		return historyId;
		
	}
	
	/**
	 * 插入测试用例结果
	 * @param testCaseResultMapper
	 * @param testCaseList
	 * @param taskQueue
	 */
//	private void insertTestCaseResult(TestCaseResultMapper testCaseResultMapper,JSONArray testCaseList,TestTaskResult taskResult) throws Exception{
//		if (testCaseList.size() > 0) {
//			for (int j = 0; j < testCaseList.size(); j++) {
//				TestCaseResult testCaseResult = new TestCaseResult();
//				JSONObject testCase = testCaseList.getJSONObject(j);
//				testCaseResult.setTaskresultid(taskResult.getId());
//				testCaseResult.setTestcaseid(Integer.valueOf(testCase.get("id").toString()));
//				testCaseResult.setCreatetime(new Date());
//				testCaseResult.setResult(DatasEnum.AutoCaseStatus_NotRun.getValue());
//				testCaseResult.setIsactive(true);
//				testCaseResultMapper.insert(testCaseResult);
//			}
//		}
//	}
	

	/**
	 * 插入测试历史记录
	 * @param taskQMapper
	 * @param testTaskResultMapper
	 * @param testCaseMapper
	 * @param taskQ
	 * @param task
	 * @param taskId
	 * @param buildparameterid
	 * @throws Exception
	 */
	private JSONObject inertTestTaskResult(JSONObject taskQueue,Integer historyId ,Integer total,Integer parentID) throws Exception{
		String uuid = taskQueue.getString("TaskUUID");		
		JSONObject params = new JSONObject();
		params.put("Total", total);
		params.put("TaskHistoryID", historyId);
		params.put("Total", total);
		params.put("Pass", 0);
		params.put("Fail", 0);
		params.put("Aborted", 0);
		params.put("ParentResultID", parentID);
		params.put("RuntimeEnv", getEnvID(taskQueue));
		params.put("TaskUUID", uuid);
		params.put("Status", DatasEnum.TaskInQueueStatus_NoAssign.getValue());
		System.out.println(params);
		JSONObject actual = HttpClientHelperBasic.postobj(Constants.API.POST_AUTO_TESTING_RESULTS, params);
		System.out.println(actual);		
		Map<String, String> paramsget = new HashMap<String, String>();
		paramsget.put("TaskUUID", uuid);
		JSONObject actualget = HttpClientHelperBasic.get(Constants.API.POST_AUTO_TESTING_RESULTS, paramsget);
		JSONObject results = actualget.getJSONObject("result").getJSONArray("results").getJSONObject(0);	
		return results;

	}
	
	private Integer getEnvID(JSONObject taskQueue) throws Exception{
		HttpClientHelper http = new HttpClientHelper();
		JSONObject taskInfoResult =http.getTaskInfo(taskQueue.getInt("TaskID"), taskQueue.getInt("TaskType"));
		TaskConfig taskConfig = TaskConfig.fromJson(taskInfoResult.getJSONObject("task_config"));
		int envID = 0;
		for (TaskStep taskStep : taskConfig.getAllSteps()) {
			if (taskStep.getType() == 12) {//plagins id待定
				envID = Integer.valueOf(taskStep.getParam("auto_host_info"));
			}			
		}
		return envID;
	}
	
	
////	/**
////	 * 任务拆分
////	 * @param taskQId
////	 * @param configId
////	 * @param taskId
////	 * @param taskUUid
////	 * @param priority
////	 * @param cmd
////	 */
////	private void testCaseSplited(CITaskMapper taskMapper,TaskQueueMapper taskQueueMapper,TestCaseMapper testCaseMapper,CITaskHistoryMapper historyMapper, TestTaskResultMapper testTaskResultMapper,TestCaseResultMapper testCaseResultMapper,TaskQueue taskQueue){
////		
////		
////	}
//		
//	
//
//	
////	/**
////	 * 拆分List
////	 * @param targe
////	 * @param size
////	 * @return
////	 */
////	private List<List<TestCase>> splitCaseList(List<TestCase> targe,int size,int splitCount) {  
////        List<List<TestCase>> listArr = new ArrayList<List<TestCase>>();  
////        //获取被拆分的数组个数  
////        int arrSize = targe.size()%size==0?targe.size()/size:targe.size()/size;  
////        for(int i=0;i<arrSize;i++) {  
////            List<TestCase>  sub = new ArrayList<TestCase>();  
////            //把指定索引数据放入到list中  
////            for(int j=i*size;j<=size*(i+1)-1;j++) { 
////                if(j<=targe.size()-1) {  
////                    sub.add(targe.get(j));  
////                }  
////            }  
////            listArr.add(sub);
////        }
////        int realsize = size*splitCount;
////        if (targe.size() > realsize) {
////	        for (int i = realsize; i < targe.size(); i++) {
////	        	 listArr.get(0).add(listArr.size(),targe.get(i));
////			}
////		}
////        return listArr;  
////    }
	
	
	public static List<List<String>> split(List<String> targe,int size,int splitCount) {  
        List<List<String>> listArr = new ArrayList<List<String>>();  
        //获取被拆分的数组个数  
        int arrSize = targe.size()%size==0?targe.size()/size:targe.size()/size;  
        for(int i=0;i<arrSize;i++) {  
            List<String>  sub = new ArrayList<String>();  
            //把指定索引数据放入到list中  
            for(int j=i*size;j<=size*(i+1)-1;j++) { 
                if(j<=targe.size()-1) {  
                    sub.add(targe.get(j));  
                }  
            }  
            listArr.add(sub);
        }
        int realsize = size*splitCount;
        if (targe.size() > realsize) {
	        for (int i = realsize; i < targe.size(); i++) {
	        	 listArr.get(0).add(listArr.size(),targe.get(i));
			}
		}
        return listArr;  
    }
	
	 public static void main(String[] args) {  
	        List<String> tarArr = new ArrayList<String>();  
	        tarArr.add("a");  
	        tarArr.add("b");  
	        tarArr.add("c");  
	        tarArr.add("d");  
	        tarArr.add("e");  
	        tarArr.add("f");  
	        tarArr.add("g");  
	        tarArr.add("h");  
	          
	        List<List<String>> result = split(tarArr, 3,3);  
	          
	        for(List<String> subArr:result) {  
	            for(String str:subArr) {  
	                System.out.println(str);  
	            }  
	       }            
	  }  
}
