package cn.teamcat.doreamon.controller.tools;

import java.io.File;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.Properties;

import javax.mail.BodyPart;
import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.Multipart;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeBodyPart;
import javax.mail.internet.MimeMessage;
import javax.mail.internet.MimeMultipart;
import javax.mail.internet.MimeUtility;


public class MailSender {
	    
    private String host;  
    private String auth;  
    private String username;  
    private String address;  
    private String password;  
    
    public MailSender(String host, String auth, String address, String username, String password) {  
        super();  
        this.host = host;  
        this.auth = auth;  
        this.address = address;  
        this.username = username;  
        this.password = password;  
    }  
    
    public void send(String[] to, String subject, String content, List<MimeBodyPart> partList) throws MessagingException, UnsupportedEncodingException {  
        Properties props = new Properties();  
        props.put("mail.smtp.host", host); 
        props.put("mail.smtp.port", 25);
        props.put("mail.smtp.auth","false");  
        Session s = Session.getDefaultInstance(props);  
        //      s.setDebug(true);  
        MimeMessage message = new MimeMessage(s);  
        InternetAddress from = new InternetAddress(address);  
        message.setFrom(from);  
        InternetAddress[] Toaddress = new InternetAddress[to.length];  
        for (int i = 0; i < to.length; i++)  
            Toaddress[i] = new InternetAddress(to[i]);  
        message.setRecipients(Message.RecipientType.TO, Toaddress);  
  
//        if (cc != null) {  
//            InternetAddress[] Ccaddress = new InternetAddress[cc.length];  
//            for (int i = 0; i < cc.length; i++)  
//                Ccaddress[i] = new InternetAddress(cc[i]);  
//            message.setRecipients(Message.RecipientType.CC, Ccaddress);  
//        }  
//  
//        if (bcc != null) {  
//            InternetAddress[] Bccaddress = new InternetAddress[bcc.length];  
//            for (int i = 0; i < bcc.length; i++)  
//                Bccaddress[i] = new InternetAddress(bcc[i]);  
//            message.setRecipients(Message.RecipientType.BCC, Bccaddress);  
//        }  
        message.setSubject(subject);  
        message.setSentDate(new Date());  
  
        BodyPart mdp = new MimeBodyPart();  
        mdp.setContent(content, "text/html;charset=UTF-8");  
        Multipart mm = new MimeMultipart();  
        if (partList != null) {
        	if (partList.size()>0) {
				for (int i = 0; i < partList.size(); i++) {
					mm.addBodyPart(partList.get(i));
				}
			}
		}
        mm.addBodyPart(mdp);  
        message.setContent(mm);  
        message.saveChanges();       
        Transport transport = s.getTransport("smtp");  
        transport.connect(host, (null == username) ? username : username, password); 
        
        transport.sendMessage(message, message.getAllRecipients());  
        transport.close();  
    }  
    
    public List<MimeBodyPart> setAttachments(List<Map<String,String>> pathList) throws IOException, MessagingException{
    	List<MimeBodyPart> partList = new ArrayList<>();
    	for (int i = 0; i < pathList.size(); i++) {
    		MimeBodyPart part = new MimeBodyPart();
    		Map<String, String> pathMap = pathList.get(i);
    		part.attachFile(new File(pathMap.get("path")));
    		part.setFileName(MimeUtility.encodeText(pathMap.get("cid")));
    		part.setContentID(pathMap.get("cid"));
   		 	partList.add(part);
		}
    	return partList;
   }
    
    
    
//    
//    public static void main(String[] args) {
//    	MailSender s = new MailSender("mail.oa.??.com", "true", "oa/??", "??.com", "hsbgm9");
//    	List<Map<String,String>> pathList = new  ArrayList<Map<String,String>>();
//    	Map<String, String> path = new HashMap<String, String>();
//    	path.put("path", "res/0.jpg");
//    	path.put("cid", "0");
//    	Map<String, String> path2 = new HashMap<String, String>();
//    	path2.put("path", "res/1.jpg");
//    	path2.put("cid", "1");
//    	pathList.add(path);
//    	pathList.add(path2);
//    	try {
//    		List<MimeBodyPart> partList = setAttachments(pathList);
//    		partList.get(0).getContentID();
//    		System.out.println(partList.get(0).getContentID());
//    		System.out.println(partList.get(1).getContentID());
//    		String mail = ReportMaker.getEmailTemplate("res/test.html").replace("$CID0",partList.get(0).getContentID()).replace("$CID1",partList.get(1).getContentID());
//			s.send(new String[]{"zhangsirui@??.com"},"测试用", mail,partList);
//		} catch (Exception e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//		}
//	}
//    
//		/**
//	  * 发送邮件的props文件
//	  */
//	 private final transient Properties props = System.getProperties();
//	 /**
//	  * 邮件服务器登录验证
//	  */
//	 private transient MailAuthenticator authenticator;
//	
//	 /**
//	  * 邮箱session
//	  */
//	 private transient Session session;
//	
//	 /**
//	  * 初始化邮件发送器
//	  * 
//	  * @param smtpHostName
//	  *                SMTP邮件服务器地址
//	  * @param username
//	  *                发送邮件的用户名(地址)
//	  * @param password
//	  *                发送邮件的密码
//	  */
//	 public SimpleMailSender(final String smtpHostName, final String username,
//	     final String password) {
//	 init(username, password, smtpHostName);
//	 }
//	
//	 /**
//	  * 初始化邮件发送器
//	  * 
//	  * @param username
//	  *                发送邮件的用户名(地址)，并以此解析SMTP服务器地址
//	  * @param password
//	  *                发送邮件的密码
//	  */
//	 public SimpleMailSender(final String username, final String password) {
//	 //通过邮箱地址解析出smtp服务器，对大多数邮箱都管用
//	 final String smtpHostName = "smtp." + username.split("@")[1];
//	 init(username, password, smtpHostName);
//	
//	 }
//	
//	 /**
//	  * 初始化
//	  * 
//	  * @param username
//	  *                发送邮件的用户名(地址)
//	  * @param password
//	  *                密码
//	  * @param smtpHostName
//	  *                SMTP主机地址
//	  */
//	 private void init(String username, String password, String smtpHostName) {
//	 // 初始化props
//	 props.put("mail.smtp.auth", "true");
//	// props.put("mail.smtp.port", "587");
//	 props.put("mail.smtp.host", smtpHostName);
//	 // 验证
//	 authenticator = new MailAuthenticator(username, password);
//	 // 创建session
//	 session = Session.getInstance(props, authenticator);
//	 }
//	
//	 /**
//	  * 发送邮件
//	  * 
//	  * @param recipient
//	  *                收件人邮箱地址
//	  * @param subject
//	  *                邮件主题
//	  * @param content
//	  *                邮件内容
//	  * @throws AddressException
//	  * @throws MessagingException
//	  */
//	 public void send(String recipient, String subject, Object content)
//	     throws AddressException, MessagingException {
//	 // 创建mime类型邮件
//	 final MimeMessage message = new MimeMessage(session);
//	 // 设置发信人
//	 message.setFrom(new InternetAddress(authenticator.getUsername()));
//	 // 设置收件人
//	 message.setRecipient(RecipientType.TO, new InternetAddress(recipient));
//	 // 设置主题
//	 message.setSubject(subject);
//	 // 设置邮件内容
//	 message.setContent(content.toString(), "text/html;charset=utf-8");
//	 // 发送
//	 Transport.send(message);
//	 }
//	
//	 /**
//	  * 群发邮件
//	  * 
//	  * @param recipients
//	  *                收件人们
//	  * @param subject
//	  *                主题
//	  * @param content
//	  *                内容
//	  * @throws AddressException
//	  * @throws MessagingException
//	  */
//	 public void send(List<String> recipients, String subject, Object content)
//	     throws AddressException, MessagingException {
//	 // 创建mime类型邮件
//	 final MimeMessage message = new MimeMessage(session);
//	 // 设置发信人
//	 message.setFrom(new InternetAddress(authenticator.getUsername()));
//	 // 设置收件人们
//	 final int num = recipients.size();
//	 InternetAddress[] addresses = new InternetAddress[num];
//	 for (int i = 0; i < num; i++) {
//	     addresses[i] = new InternetAddress(recipients.get(i));
//	 }
//	 message.setRecipients(RecipientType.TO, addresses);
//	 // 设置主题
//	 message.setSubject(subject);
//	 // 设置邮件内容
//	 message.setContent(content.toString(), "text/html;charset=utf-8");
//	 // 发送
//	 Transport.send(message);
//	 }
//	 

} 


