package cn.teamcat.doreamon.controller.tools;

import java.util.List;

import cn.teamcat.doraemon.controller.db.dict.DatasEnum;

/**
 * 任务状态控制
 * @author Sirui.Zhang
 *
 */
public class TaskStatusController {
	
//	/**
//	 * 从任务队列及任务List删除任务，并更改任务为完成状态，需要在队列循环中使用
//	 * @param task
//	 * @param taskQ
//	 * @param taskQueIdList  
//	 * @param i 队列中位置
//	 */
//	public void deleteTaskAndUpdateStatus(String TQTaskUUID,int taskQueId,int taskId){
//		Constants.task.updateTaskStatus(taskId, DatasDict.AutoTaskStatus_Completed);
//		Constants.taskQ.delectTaskByUUid(TQTaskUUID);
//	}
//	
//	
	/**
	 * 判断兄弟任务是否完成
	 * @param taskQ
	 * @param broTaskQList
	 * @return
	 */
//	public static boolean isSubtaskFinished(List<TaskQueue> subtaskQueueList){
//		boolean finished = false;
//		for (int i = 0; i < subtaskQueueList.size(); i++) {
//			int taskQStatus = subtaskQueueList.get(i).getStatus();
//			if (taskQStatus == DatasEnum.TaskInQueueStatus_Complete.getValue() || taskQStatus == DatasEnum.TaskInQueueStatus_AssignFail.getValue() 
//					||taskQStatus == DatasEnum.TaskInQueueStatus_Aborted.getValue() || taskQStatus == DatasEnum.TaskInQueueStatus_Error.getValue() 
//					|| taskQStatus == DatasEnum.TaskInQueueStatus_Timeout.getValue() ) {
//				finished = true;
//			}else{
//				finished = false;
//				break;
//			}
//		}
//		return finished;
//	}
//	
	


//	
//	/**
//	 * 判断兄弟任务是均为超时
//	 * @param taskQ
//	 * @param broTaskQList
//	 * @return
//	 */
//	public boolean isTaskListStatus(List<TaskQueue> broTaskQList, int status){
//		boolean finished = true;
//		for (int i = 0; i < broTaskQList.size(); i++) {
//			int broStatus = Constants.taskQ.getTaskStatus(Integer.valueOf(broTaskQList.get(i).toString()));
//			if (broStatus == status) {
//				finished = true;
//			}else{
//				finished = false;
//			}
//		}
//		return finished;
//	}	
	
//	/**
//	 * 判断任务状态
//	 * @param taskQStatus
//	 * @return
//	 */
//	public boolean isTaskStatus(int taskQStatus,int status){
//		boolean noProcess = false;
//		if (taskQStatus == status) {
//			noProcess = true;
//		}else{
//			noProcess = false;
//		}
//		return noProcess;
//	}
	
	/**
	 * 判断任务是否完成
	 * @param taskQStatus
	 * @return
	 */
	public static boolean isFinished(int taskQStatus){
		boolean finished = false;
		if (taskQStatus == DatasEnum.TaskInQueueStatus_Complete.getValue() || taskQStatus == DatasEnum.TaskInQueueStatus_AssignFail.getValue() 
				||taskQStatus == DatasEnum.TaskInQueueStatus_Aborted.getValue() || taskQStatus == DatasEnum.TaskInQueueStatus_Error.getValue() 
				|| taskQStatus == DatasEnum.TaskInQueueStatus_Timeout.getValue() ){
			finished = true;
		}else{
			finished = false;
		}
		return finished;
	}

	
//	/** 
//	 * 获取RuntimeEnv
//	 * @param config
//	 * @param configId
//	 * @return
//	 */
//	public String getRuntimeEnv(int configId){
//		String trruntimeEnv = "";
//		int taskType =Constants.config.getTaskType(configId);
//		if (taskType == DatasDict.AutoTaskType_APPUI) {
//			trruntimeEnv = Constants.config.getOsTpye(configId).toString();
//		}else if (taskType == DatasDict.AutoTaskType_WebUI) {
//			trruntimeEnv =Constants.config.getBrowser(configId).toString();
//		}else{
//			trruntimeEnv ="Interface";
//		}
//		return trruntimeEnv;
//	}
	
}
