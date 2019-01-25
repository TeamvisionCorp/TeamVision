package com.xracoon.teamcat.agent.config;

import java.util.ArrayList;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;
import org.apache.log4j.AppenderSkeleton;
import org.apache.log4j.spi.LoggingEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.xracoon.teamcat.agent.app.Agent;
import com.xracoon.teamcat.agent.webservice.AgentWebService;
import com.xracoon.util.basekit.StringEx;

public class TeamcatAppender extends AppenderSkeleton{
	Logger logger= LoggerFactory.getLogger(TeamcatAppender.class);
	private String ENTER = "{ENTER}"; 
	private String END =  "{THE END}";
	private String RETURN="</br>";
	private final long taskQueueId;
	private final int cacheListSize;
	private final int cacheTime; //5sec
	private List<String> cacheList = new ArrayList<>();  
	private Boolean isLogDone = false;
	private Timer timer;
	
	public TeamcatAppender(long tqID){
		this(tqID, 2000,10);
	}
	public TeamcatAppender(long tqID, int cacheCount, int cacheSeconds) {
		this.taskQueueId=tqID;
		this.cacheListSize=cacheCount;
		this.cacheTime=cacheSeconds*1000;
		timer = new Timer();
		timer.schedule(new RemindTask(), cacheTime, cacheTime);
	}

	@Override
	public void close() {
	}

	@Override
	public boolean requiresLayout() {
		return false;
	}

	@Override
	public void append(LoggingEvent event) {
		String log = this.layout.format(event);
		try {
			//如果已经设置结束标志，不再缓存
			if(isLogDone){
				AgentWebService.andMessage(taskQueueId, log);
				return;
			}
				
			if (log.contains(END)) {
				timer.cancel();
				sendAllLog(log);
				isLogDone = true;
			}else{
				if (cacheList.size() >= cacheListSize-1) {
					sendAllLog(log);
				}else{
					synchronized(this){
						cacheList.add(log);
					}
				}
			}
		} catch (Exception e) {
			logger.error(e.getMessage(), e);
		}
	}
	
	
	
	synchronized private String getCacheListLog(){
		StringBuilder sbuf = new StringBuilder();
		for (int i = 0; i < cacheList.size(); i++) 
		{
			String temp=cacheList.get(i);
			if (temp.toUpperCase().contains("[ERROR]"))
			{
				temp="<strong style='color:red;font-size:18px;'>"+temp+"</strong>";
			}
			sbuf.append(temp).append(RETURN);
		}
		cacheList.clear();
		if(sbuf.length()>0)
			sbuf.delete(sbuf.length()-ENTER.length(), sbuf.length());
		return sbuf.toString();
	}
	
	private void sendAllLog(String log) throws Exception{
		Boolean result=AgentWebService.andMessage(taskQueueId, getCacheListLog()+ (log!=null? RETURN+log:""));
//		Boolean result=true;
		if (!result) 
		{
			logger.info("日志推送失败:" + log);
		}
	}

	public Boolean IsLogDone() {  
		return isLogDone;  
	}  
	public String getEndTag(){
		return END;
	}
	public void setEndTag(String endTag){
		END= endTag;
	}
	 
	class RemindTask extends TimerTask {
        public void run() {
        	String log = getCacheListLog();
//        	Boolean result=true;
        	if (!StringEx.isBlank(log)) {
        		try {
        			Boolean result=AgentWebService.andMessage(taskQueueId, log);
					if (!result) {
						logger.info("日志推送失败:" + log);
					}
				} catch (Exception e) {
					logger.error(e.getMessage(), e);
				}
			}
        }
    }
}
