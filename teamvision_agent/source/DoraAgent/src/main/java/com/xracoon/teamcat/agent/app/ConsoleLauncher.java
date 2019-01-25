package com.xracoon.teamcat.agent.app;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;
import java.util.Scanner;
import org.apache.log4j.Logger;
import org.apache.log4j.PropertyConfigurator;

import com.xracoon.teamcat.agent.config.AgentConfig;
import com.xracoon.teamcat.agent.config.ConfigLoader;
import com.xracoon.teamcat.agent.testclient.NetClient;
import com.xracoon.util.basekit.FilesEx;
import com.xracoon.util.basekit.StringEx;
import com.xracoon.util.basekit.system.OS;

/**
 * Agent控制台启动类
 * 
 * @author Yangtianxin
 */
public class ConsoleLauncher {
	public static String basePath="";
	public static boolean isDebug=false;
	static {
		basePath=System.getProperty("user.dir");
		if(isDebug){
			basePath=basePath+"/source/DoraAgent/";
		}else{
			basePath=basePath+"/";
		}
		//String home=FilesEx.locateHome("log4j.properties");
		PropertyConfigurator.configure(basePath+"log4j.properties");
		//PropertyConfigurator.configure("/home/gaozhenbin/workcodes/teamcat_agent/source/DoraAgent/log4j.properties");
	}
	static final Logger logger = Logger.getLogger(ConsoleLauncher.class);
	
	static public void forceStop() {

	}

	static public void main(String[] args) {
		ConsoleLauncher launcer=new ConsoleLauncher();
		
		try {
			Runtime.getRuntime().addShutdownHook(new Thread() {
				public void run() {
					logger.error("Unexcepted Terminate Occour");
					forceStop();
				}
			});
			
			if(args.length>0){
				if (!args[0].toLowerCase().equals("client")) 
					launcer.launchAgent(args[0]);
				else
					launcer.clientLoop();
			}
			else{
				String agentKey=null;
				InputStream is=null;
				try{
					//String configFile= FilesEx.locateHome("agent.properties");
					//String configFile="/home/gaozhenbin/workcodes/teamcat_agent/source/DoraAgent/";
					if(!StringEx.isBlank(basePath)){
						File file=new File(basePath, "agent.properties");
						is= FilesEx.openInputStream(file.getAbsolutePath());
						Properties prop = new Properties();
						prop.load(is);
						if(prop.containsKey("agent.key") 
								&& !StringEx.isBlank(agentKey=prop.getProperty("agent.key").trim())){
						}
					}	
				}finally{
					if(is!=null)
						try { is.close(); } 
						catch (IOException e1) {}
				}
				
				if(!StringEx.isBlank(agentKey))
					launcer.launchAgent(agentKey);
				else
					throw new Exception("'agent identity-key' not found in start command or in agent.properties file");
			}
			
			// HibernateUtil.closeFactory();
			logger.info("==>launch done");
		} catch (Exception ex) {
			logger.error(ex.getMessage(), ex);
		}
	}
	
	public void singleCmd()
	{
		
	}
	
	public void clientLoop()
	{
		logger.info("start client......");
		System.out.println(">send cmd: ");

		Scanner sc = new Scanner(System.in);
		OS os = OS.getNewInstance();
		while (sc.hasNext()) {
			String cmd = sc.nextLine().trim();
			if (cmd.equals("EXIT") || cmd.equals("QUIT"))
				break;

			NetClient client = new NetClient(os.getIP(null), 5001, cmd+ "\n");
			// 不开新线程
			client.run();
			
			System.out.println(">send cmd: ");
		}
		sc.close();
		logger.info("client quit");
	}
	
	public void launchAgent(String key)
	{
		logger.info("\n\n=============================\nTeamcat Agent\n=============================");
		//String agentHome=FilesEx.locateHome("libs");
		//String agentHome="/home/gaozhenbin/workcodes/teamcat_agent/source/DoraAgent/";
		logger.info(basePath);
		if(basePath==null){
			logger.error("AgentHome not found!");
			System.exit(-1);
		}
		
		String configPath = basePath + "agent.properties";
		ConfigLoader configLoader = new ConfigLoader();
		AgentConfig config = configLoader.load(configPath);
		config.agentHome=basePath;
		config.agentKey=key;
		
		logger.info("start server......");

		Agent agent = null;
		try {
			agent = new Agent(config);
			agent.start();
		} catch (Exception e) {
			logger.error(e.getMessage(), e);
			forceStop();
			return;
		}
	}
}
