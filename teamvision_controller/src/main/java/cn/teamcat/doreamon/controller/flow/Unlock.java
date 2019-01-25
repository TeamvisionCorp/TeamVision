package cn.teamcat.doreamon.controller.flow;

import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Locale;

import org.apache.http.protocol.HTTP;
import org.apache.ibatis.session.SqlSession;
import org.apache.log4j.Logger;

import cn.teamcat.doraemon.controller.db.dict.DatasEnum;
import cn.teamcat.doreamon.controller.config.TimeoutConfig;
import cn.teamcat.doreamon.controller.tools.CommonUtil;
import cn.teamcat.doreamon.controller.tools.HttpClientHelper;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

/**
 * 解锁超时锁定任务
 * @author Sirui.Zhang Siyuan.Lu
 *
 */
public class Unlock {
	Logger log = Logger.getLogger(Unlock.class);
    HttpClientHelper http = new HttpClientHelper();
	/**
	 * 解锁锁定超时任务
	 * @param session
	 * @throws Exception 
	 */
	public void unlockQueue() throws Exception{
		log.info("Controller-Unlock-开始运行");
		JSONObject response = http.getLockedTaskqueues();
		JSONArray taskQueuelist = response.getJSONArray("result");
		System.out.println(taskQueuelist);
		for (int i = 0; i < taskQueuelist.size(); i++) {
			Integer taskQueueId = taskQueuelist.getJSONObject(i).getInt("id");
			try {
				String LockTimeStr = taskQueuelist.getJSONObject(i).getString("LockTime");
				if (!LockTimeStr.equals(null)) {
					LockTimeStr = LockTimeStr.replace("000+08:00", " CST");
					SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss.SSS Z");
					Date d = format.parse(LockTimeStr);
					long lockTime =  d.getTime();
					if (isTimeout(lockTime)) {			 
						http.unlocktask(taskQueueId);
						log.info("Controller-Unlock-已将 taskQueueId："+taskQueueId+"任务解锁");
					}
				}
			} catch (Exception e) {
				log.info("任务"+taskQueueId+"没有处理，无locktime");
			}
		}
		log.info("Controller-Unlock-运行完毕");
	}
	
	private  boolean isTimeout(long queueTime){
		TimeoutConfig timeout = new TimeoutConfig();
		Calendar calendar = Calendar.getInstance(Locale.CHINA);
        Date nowdate = calendar.getTime();     		
		long  time = nowdate.getTime() - queueTime;
		if (time>timeout.getLockTimeout()) {
			log.info("Controller-Unlock-当前有锁定超时任务");
			return true;
		}else{
			return false;
		}
	}
}
