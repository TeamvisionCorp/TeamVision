package com.xracoon.teamcat.agent.network;

import java.net.ServerSocket;
import java.net.Socket;
import java.util.Properties;

import com.xracoon.teamcat.agent.utils.PropertiesTools;
import org.apache.log4j.Logger;

import com.xracoon.teamcat.agent.app.Agent;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

/**
 * Socket网络服务监听线程
 * @author Yangtianxin
 */
public class NetServer extends Thread {

	private final JedisPool jedisPool;
	private int port;
	private Agent agent;
	private Logger logger = Logger.getLogger("netMonLogger");
	private ServerSocket server;
	private final String channel = "CI_AGENT_"+PropertiesTools.getProperty("agent.key");
	
	public NetServer(Agent agent,JedisPool jedisPool) {
		super(agent,"NetServerThread");
		this.agent=agent;
		this.port = agent.getAgentConfig().agentPort;
		this.jedisPool=jedisPool;
	}

	public void run() {
		// Start Socket listener
		Jedis jedis=jedisPool.getResource();
		try {
			while (!this.isInterrupted())
			{

				logger.debug("accept connect");
				
				NetCmdExecutor netExecutor=new NetCmdExecutor();
				netExecutor.addNetCmdListener(agent);
				jedis.subscribe(netExecutor,channel);
			}
		} catch (Exception e) {
			logger.error("服务端Socket运行异常:"+port+":"+e.getMessage(), e);
		}finally {
			jedis.close();
		}
	}
	
	public void shutdown()
	{
		if (server != null) {    
            try {    
            	server.close();
            	server = null;
    			logger.info(">server stoped");
            } catch (Exception e) {    
            	logger.error("服务端Socket关闭异常:"+e.getMessage(), e);  
            }    
        }  
	}
}
