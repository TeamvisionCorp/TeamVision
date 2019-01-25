package com.xracoon.teamcat.driver;

import java.io.File;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.xracoon.util.basekit.FilesEx;

public  class WebApiArchiveManager implements ArchiveManager {
	public TaskInfo info;
	private Logger logger = LoggerFactory.getLogger(WebApiArchiveManager.class);
	public WebApiArchiveManager(TaskInfo info){
		this.info=info;
	}
	
	@Override
	public void setLogger(Logger logger){
		this.logger=logger;
	}
	
	public boolean isFileAvailable(File file){
		long maxSize=2048;//最大不能超过2048M
/*		if(file.length()==0)
		{
			logger.info(file.getName()+":  size is 0");
			return false;
		}
		else*/ 
		logger.info("file size is: "+String.valueOf(file.length()));
		long fileSize=file.length()/(1024*1024);
		logger.info("file size is: "+String.valueOf(fileSize)+"M");
		if(fileSize>maxSize)
		{
			logger.info(file.getName()+":  too large >"+FilesEx.getBriefSize(maxSize));
			return false;
		}	
		
		return true;
	}
	
	@Override
	public boolean processArchiveRequest(String file, int type) {
		try {
			File f=new File(file);
			if(f.exists() && isFileAvailable(f)){
				return WebService.tqUpload(info.taskQueueID, file, type);
				//return true;
			}
		} catch (Exception e) {
			logger.error(e.getMessage(), e);
		}
		return false;
	}
}
