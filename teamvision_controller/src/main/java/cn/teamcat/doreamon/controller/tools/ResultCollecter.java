package cn.teamcat.doreamon.controller.tools;

//import org.apache.log4j.Logger;

/**
 * 测试结果收集
 * @author Sirui.Zhang
 *
 */
public class ResultCollecter {
//	private Logger log = Logger.getLogger(ResultCollecter.class);
//		
//	/**
//	 * 根据子任务信息更改父任务信息
//	 * @param taskQueId
//	 * @param taskId
//	 * @param Uuid
//	 * @param trstatus
//	 * @return 父任务结果ID
//	 */
//	public int parentCollect(int taskQueId,int taskId,String Uuid,int trstatus){
//		log.info("父任务的Uuid:"+Uuid);
//		int parentTaskRunId = Constants.taskR.getTaskrunResultID(Uuid, false);
//		if (parentTaskRunId !=0) {
//			parent(parentTaskRunId, Uuid,trstatus);
//		}else{
//			ProjectVersionService project = new ProjectVersionService();
//			int configId = Constants.task.getTaskConfigId(taskId);
//			String trprojectVersion = project.getVersion(Constants.config.getTCFProjectVersion(configId));
//			Constants.taskR.addTestrunResult(taskId,getSubString(Constants.taskQ.getCaseList(taskQueId), ","), Uuid, 0, 0,Constants.taskCtrl.getRuntimeEnv(configId), 0, trprojectVersion, Constants.taskQ.isChild(taskQueId));
//			parentTaskRunId = Constants.taskR.getTaskrunResultID(Uuid, false);
//			parent(parentTaskRunId, Uuid,trstatus);
//		}
//		return parentTaskRunId ;
//	}
//	
//	private void parent(int parentTaskRunId,String Uuid,int trstatus){
//		log.info("父任务的TaskRunId"+parentTaskRunId);
//		int trpass = 0;
//		int trfail = 0;
//		int traborted = 0;
//		String trerror = "";
//		List<?> taskRIdList = Constants.taskR.getTaskRunChildIDList(Uuid);		
//		for (int i = 0; i < taskRIdList.size(); i++) {
//			int sunTaskRid = Integer.valueOf(taskRIdList.get(i).toString());
//			System.out.println("sunTaskRid: "+ sunTaskRid);
//			Map<String, Object> taskRInfo = Constants.taskR.queryTaskRunInfo(sunTaskRid);
//			trpass = trpass+Integer.valueOf(taskRInfo.get("passed").toString());
//			trfail = trfail+Integer.valueOf(taskRInfo.get("failed").toString());;
//			traborted = traborted+Integer.valueOf(taskRInfo.get("aborted").toString());
//			if (trerror != "null") {
//				if (taskRInfo.get("errorMsg") != null) {
//					String error = taskRInfo.get("errorMsg").toString();
//					if (error.length() > 30) {
//						error = error.substring(0, 30)+"...";
//						trerror = trerror+error+",";
//					}
//					trerror = trerror.replace("null", "");
//				}
//				
//			}
//		}
//		if (getSubString(trerror, ".")>1) {//输入errorMsg 中.多余1个便认为该
//			trerror = trerror.replace("Task", "One of task");
//		}
//		Constants.taskR.updateTestrunResult(parentTaskRunId, trpass, trfail, traborted,Constants.taskR.getTaskRunStartTime(Uuid), Constants.taskR.getTaskRunEndTime(Uuid), trstatus, trerror);
//	}
//	
//	
//	
//	/**
//	 * 计数器
//	 * @param str
//	 * @param key
//	 * @return
//	 */
//	public int getSubString(String str,String key){
//        int count = 0;
//        int index = 0;
//        while((index=str.indexOf(key,index))!=-1){
//            index = index+key.length();
//            count++;
//        }
//        return count;
//    }
//	
//	/**
//	 * 更改收集任务结果
//	 * @param taskId
//	 * @param taskQueId
//	 * @param Uuid
//	 * @param agentId
//	 * @return 任务结果ID
//	 */
//	public Integer collect(int taskId,int taskQueId ,String Uuid){
//		log.info("进入collect流程");
//		int trstatus = Constants.taskQ.getTaskStatus(taskQueId);
//		log.info("trstatus:"+trstatus);
//		String trerror =Constants.taskQ.getTaskErrorMsg(taskQueId);
//		log.info("trerror:"+trerror);
//		int trtaskRunId = Constants.taskR.getTaskrunResultID(Uuid);
//		log.info("trtaskRunId"+trtaskRunId);
//
//		if (trtaskRunId == 0) {
//			trtaskRunId = failCollect(taskQueId, taskId, Uuid, trstatus, trerror);
//		}else{//uuid case不为空才整理
//			int agentId = Constants.taskQ.getTqagentId(taskQueId);
//			passCollect(trtaskRunId, Uuid, agentId, trstatus, trerror);
//		}
//		return trtaskRunId;
//	}
//	
//	
//	private void passCollect(int trtaskRunId,String Uuid,int agentId,int trstatus ,String trerror){
//		log.info("下发成功归集流程");
//		int pass = caseR.getCaseResultId(Uuid, agentId, DatasDict.AutoCaseStatus_Pass).size();
//		log.info("pass:"+pass);
//		int fail = caseR.getCaseResultId(Uuid, agentId, DatasDict.AutoCaseStatus_Fail).size();
//		log.info("fail:"+fail);
//		Map<String, Object> taskRInfo = Constants.taskR.queryTaskRunInfo(trtaskRunId);
//		int aborted = Integer.valueOf(taskRInfo.get("total").toString()) - pass - fail;
//		log.info("aborted:"+aborted);
//		Date startTime = caseR.getARCStartTime(agentId, Uuid);
//		Date endTime = caseR.getARCEndTime(agentId, Uuid);
//		log.info("trerror:"+trerror);
//		Constants.taskR.updateTestrunResult(trtaskRunId, pass, fail, aborted, startTime, endTime, trstatus, trerror);	
//	}
//	
//	
//	private Integer sendFailCollect(int taskQueId ,int taskId , String Uuid,int trstatus,String trerror){
//		log.info("下发失败归集流程");
//		log.info("trstatus: "+trstatus);
//		log.info("trerror: "+trerror);
//		ProjectVersionService project = new ProjectVersionService();
//		int trparentResultId = 0;
//		int parentId = Constants.taskR.getTaskrunResultID(Uuid, false);
//		if (parentId == 0 ) {
//			 trparentResultId = parentId;
//		}
//		int agentId =Constants.taskQ.getTqagentId(taskQueId) ;
//		int configId = Constants.task.getTaskConfigId(taskId);
//		String trprojectVersion = project.getVersion(Constants.config.getTCFProjectVersion(configId));
//		Constants.taskR.addTestrunResult(Constants.taskQ.getTaskId(taskQueId),getSubString(Constants.taskQ.getCaseList(taskQueId), ","), Uuid, trparentResultId, 0,
//		Constants.taskCtrl.getRuntimeEnv(configId), agentId, trprojectVersion, Constants.taskQ.isChild(taskQueId));
//		int trtaskRunId = Constants.taskR.getTaskrunResultID(Uuid);
//		Map<String, Object> taskRInfo = Constants.taskR.queryTaskRunInfo(trtaskRunId);
//		Constants.taskR.updateTestrunResultWithoutTime(trtaskRunId, 0, 0, Integer.valueOf(taskRInfo.get("total").toString()),trstatus, trerror);
//		return trtaskRunId;
//	}
}
