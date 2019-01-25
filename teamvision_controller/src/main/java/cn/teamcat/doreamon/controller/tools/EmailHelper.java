package cn.teamcat.doreamon.controller.tools;


import java.text.SimpleDateFormat;
import java.util.List;
import java.util.Map;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

import org.apache.log4j.Logger;

import cn.teamcat.doreamon.controller.config.EmailConfig;
  

/**
 * 邮件发送
 * @author Sirui.Zhang
 */
public class EmailHelper{
	
	private Logger log = Logger.getLogger(MailSender.class);
	
	/**
	 * 获取Email地址
	 * @param taskId
	 * @param taskType
	 * @return
	 * @throws Exception
	 */
	public String[] getEmail(Integer project) throws Exception{
		HttpClientHelper http = new HttpClientHelper();
		JSONArray menberList = http.getMemberList(project);
		String[] mailList = new String[menberList.size()];
		for (int i = 0; i < menberList.size(); i++) {
			JSONObject menber = menberList.getJSONObject(i);
			mailList[i] = menber.getString("email"); 
		}
		return mailList;
	}
	

	/**
	 *  发送邮件
	 * @param taskId
	 * @param taskType
	 * @param subject
	 * @param email
	 * @return
	 * @throws Exception
	 */
	public String sendEmailReport(Integer projectId,String subject,String content,List<Map<String,String>> pathList) throws Exception{
		log.info("EmailHelper-subject: " + subject);
		log.info("EmailHelper-email: " + content);
		try
		{
			EmailConfig mailConfig = new EmailConfig();
			MailSender mail = new 
					MailSender(mailConfig.getMailHost(), mailConfig.getMailAuth(), mailConfig.getMailAddress(), mailConfig.getMailUsername(), mailConfig.getMailPassword());
			//更改为JSONObject返回值
			String[] mailReceiver = getEmail(projectId);
		    mail.send(mailReceiver, subject, content,null);
//		if (pathList.size() <= 10) {
//			mail.send(mailReceiver, subject, content,mail.setAttachments(pathList));
//		}else{
//			mail.send(mailReceiver, subject, content,null);
//		}
		}
		catch (Exception e) {
			log.info(e.getMessage());
		}
		return "";
	}

	public String getReceiverForRTX(String[] mailReceiver) throws Exception{
		String receiver = "";
		for (int i = 0; i < mailReceiver.length; i++) {
			String[] to = mailReceiver[i].split("@");
			receiver = receiver + to[0] + ",";
		}
		return receiver.substring(0,receiver.length()-1);
	}
	
	
	public void sendEmailReport(String[] to,String subject,String content) throws Exception{
		log.info("EmailHelper-subject: " + subject);
		log.info("EmailHelper-email: " + content);
		EmailConfig mailConfig = new EmailConfig();
		MailSender mail = new MailSender(mailConfig.getMailHost(), mailConfig.getMailAuth(), mailConfig.getMailAddress(), mailConfig.getMailUsername(), mailConfig.getMailPassword());
//		MailSender mail = new MailSender(Init.MAIL_HOST, "true", Init.MAIL_USERNAME, Init.MAIL_DOMAIN_USER, Init.MAIL_PASSWORD);
		mail.send(to, subject, content,null);
	}
    
	

	/**
	 * 发送异常邮件
	 * @param task
	 * @throws Exception
	 */
//	public void sendErrorMail(JSONObject task) throws Exception{
//		EmailConfig mailConfig = new EmailConfig();
//		String taskName = task.getTaskname();
//		String subject = "Timer-["+taskName+"]插入失败";
//		String content = ReportMaker.getEmailTemplate("res/TimerErrorReport.html");
//		content = content.replace("$Subject", subject);
//		content = content.replace("$TaskName", taskName);	
//		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
//		content = content.replace("$LastRunTime", sdf.format(task.getLastruntime()));
//		sendEmailReport(mailConfig.getDefaultMailRecivers().split(","), subject, content);
//	}
	/**
	 * 发送异常邮件
	 * @param task
	 * @throws Exception
	 */
	public void sendErrorMail(JSONObject task) throws Exception{
		EmailConfig mailConfig = new EmailConfig();
		String taskName = task.getString("TaskName");
		String subject = "Timer-["+taskName+"]插入失败";
		String content = ReportMaker.getEmailTemplate("res/TimerErrorReport.html");
		content = content.replace("$Subject", subject);
		content = content.replace("$TaskName", taskName);	
		SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
		content = content.replace("$LastRunTime", sdf.format(task.getString("LastRunTime")));
		sendEmailReport(mailConfig.getDefaultMailRecivers().split(","), subject, content);
	}
	
}
