package cn.teamcat.doreamon.controller.flow;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

import org.apache.log4j.Logger;
import org.apache.ibatis.session.SqlSession;

import com.google.gson.JsonArray;

import cn.teamcat.doraemon.controller.db.dict.DatasEnum;
import cn.teamcat.doreamon.controller.config.EmailConfig;
import cn.teamcat.doreamon.controller.config.GlobalConfig;
import cn.teamcat.doreamon.controller.tools.Constants;
import cn.teamcat.doreamon.controller.tools.EmailHelper;
import cn.teamcat.doreamon.controller.tools.HttpClientHelper;
import cn.teamcat.doreamon.controller.tools.ReportMaker;
import cn.teamcat.doreamon.controller.tools.SessionFactoryUtil;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;
/**
 * Disaster 监控
 * @author Siyuan.Lu,Sirui.Zhang
 *
 */
public class DisasterDetecter {

	private HttpClientHelper http = new HttpClientHelper();
	private Logger log = Logger.getLogger("disaster");
	
	public void detectDisaterTask(){
		try {
			log.info("DetectDisater-开始运行");
			disaster();
			taskTooMach();
			log.info("DetectDisater-运行完毕");
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	private void taskTooMach() throws Exception{
		JSONObject taskqueuesResponse = http.getTaskqueuesbyStatus(DatasEnum.TaskInQueueStatus_NoProcess.getValue());
		JSONArray taskList = taskqueuesResponse.getJSONArray("result");
		GlobalConfig config = new GlobalConfig();
		if (taskList.size() >= config.getTaskLimit()) {
			log.info("DetectDisater-当前任务过多");
			EmailHelper email = new EmailHelper();
			EmailConfig mailConfig = new EmailConfig();
			String content = ReportMaker.getEmailTemplate("res/TaskTooMachReport.html");
			content = content.replace("$Subject", Constants.ChineseMsg.TASK_TOO_MACH_EMAIL_SUBJECT);
			email.sendEmailReport(mailConfig.getDefaultMailRecivers().split(","), Constants.ChineseMsg.TASK_TOO_MACH_EMAIL_SUBJECT, content);
			http.sendRTXMessage(mailConfig.getDefaultRtxRecivers(), Constants.ChineseMsg.TASK_TOO_MACH_EMAIL_SUBJECT, "");
		}
	}
	
	private void disaster() throws Exception{
		JSONObject taskqueuesResponse = http.getTaskqueuesbyStatus(DatasEnum.TaskInQueueStatus_Disaster.getValue());
		JSONArray disasterTaskList = taskqueuesResponse.getJSONArray("result");
		GlobalConfig config = new GlobalConfig();		
		if (disasterTaskList.size()>0) {
			log.info("DetectDisater-当前有灾难任务");
			EmailHelper email = new EmailHelper();
			EmailConfig mailConfig = new EmailConfig();
			String content = ReportMaker.getEmailTemplate("res/DisasterReport.html");
			content = content.replace("$Subject", Constants.ChineseMsg.DISASTER_EMAIL_SUBJECT);
			String summary = "";
			for (int i = 0; i < disasterTaskList.size(); i++) {
				JSONObject taskQ = disasterTaskList.getJSONObject(i);
				summary = summary + ReportMaker.getEmailTemplate("res/DisasterSummary.html");
				summary = summary.replace("$TaskQueueId", String.valueOf(taskQ.getInt("id")) );
				log.info("TaskQueueId"+taskQ.getString("id"));
				summary = summary.replace("$EnqueueTime", taskQ.getString("EnqueueTime"));
				log.info("EnqueueTime"+taskQ.getString("ErrorMsg"));
				if (taskQ.getString("ErrorMsg") != null) {
					summary = summary.replace("$ErrorMsg", taskQ.getString("ErrorMsg"));
					log.info("+++ErrorMsg:"+taskQ.getString("ErrorMsg"));
				}else{
					summary = summary.replace("$ErrorMsg", "--");
					log.info("+++ErrorMsgnull:"+taskQ.getString("ErrorMsg"));
				}
			}
			content = content.replace("$DisasterSummary", summary);
			email.sendEmailReport(mailConfig.getDefaultMailRecivers().split(","), Constants.ChineseMsg.DISASTER_EMAIL_SUBJECT, content);
			http.sendRTXMessage(mailConfig.getDefaultRtxRecivers(), Constants.ChineseMsg.DISASTER_EMAIL_SUBJECT + new Date(), "");
			log.info("complete");
		}
	}
}
