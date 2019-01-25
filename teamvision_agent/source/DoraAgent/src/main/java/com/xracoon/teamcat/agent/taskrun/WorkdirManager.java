package com.xracoon.teamcat.agent.taskrun;

import java.io.File;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.xracoon.teamcat.driver.DatasEnum;
import com.xracoon.teamcat.driver.TaskInfo;
import com.xracoon.util.basekit.FilesEx;

public class WorkdirManager {
	private Logger logger = LoggerFactory.getLogger(WorkdirManager.class);
	public void setLogger(Logger logger){
		this.logger=logger;
	}
	
	private File workDir;
	
	public File getWorkDir(){
		return workDir;
	}
	
	public WorkdirManager(String dir){
		this.workDir=new File(dir);
	}
	
	public boolean clean(){
		FilesEx.deleteContent(workDir);
		logger.info("workdir clean : "+workDir.getAbsolutePath());
		return workDir.list().length==0;
	}

	public void prepare(TaskInfo info, boolean clean) throws Exception{
		File taskDir=getTaskDir(info);
		//不存在则创建，结束
		if(!taskDir.exists()){
			taskDir.mkdirs();
			return;
		}
		//已经存在并且需要清理
		else if(clean){
			FilesEx.deleteContent(taskDir);
			//未删除成功时多次尝试
			int tryNum=1;
			while(taskDir.list().length>0 && tryNum++<5){
				FilesEx.deleteContent(taskDir);
				Thread.sleep(2000);
			}
		}

		if(clean && taskDir.list().length!=0){
			logger.warn("uncleanable file(s)");
			for(String s: taskDir.list())
				logger.warn("\t"+s);
		}
	}
	
	public boolean deleteTaskDir(TaskInfo info) throws Exception {
		File taskDir=getTaskDir(info);
		FilesEx.deleteTree(taskDir);
		//未删除成功时多次尝试
		int tryNum=1;
		while(taskDir.exists() && tryNum++<5){
			FilesEx.deleteContent(taskDir);
			Thread.sleep(2000);
		}
		
		if(taskDir.exists()) return false;
		
		if(info.taskType==DatasEnum.AutoTaskType_APPUI.getValue() && taskDir.getParentFile().exists() && (taskDir.getParentFile().list()==null || taskDir.getParentFile().list().length==0)){	
			File parentDir=taskDir.getParentFile();
			FilesEx.deleteTree(parentDir);
			//未删除成功时多次尝试
			int tryNum1=1;
			while(taskDir.exists() && tryNum1++<5){
				FilesEx.deleteContent(parentDir);
				Thread.sleep(2000);
			}
			if(parentDir.exists()) return false;
		}
		return true;
	}
	
	public File getTaskDir(TaskInfo info){
		File taskDir=null;
		if(info.taskType==DatasEnum.AutoTaskType_APPUI.getValue())
			taskDir=new File(workDir,"t"+info.taskID+"_"+info.taskConfig.getTaskName()+"/tq"+info.taskQueueID);
		else
			taskDir=new File(workDir,"t"+info.taskID+"_"+info.taskConfig.getTaskName());
		
		return taskDir;
	}
}
