package com.xracoon.teamcat.driver;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import org.apache.log4j.Logger;

/**
 * 测试客户端
 * @author Yangtianxin
 */
public class NetClient {

	private String ip;
	private int port;
	private String cmd;
	private Logger logger = Logger.getLogger(NetClient.class);
	
	
	public NetClient(String ip,int port,String cmd) {
		this.ip=ip;
		this.port = port;
		this.cmd=cmd;
	}

	public void run()
	{
		Socket socket = null;
		try {
			socket = new Socket(ip,port);
		} catch (Exception e) {
			logger.error("客户端Socket初始化异常:"+e.getMessage(), e);
		}
		
		try
		{
			BufferedReader is = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			PrintWriter os = new PrintWriter(socket.getOutputStream());
	
			logger.info("send cmd:"+cmd);
			os.write(cmd);
			os.flush();
			
			String line=null;
			while((line=is.readLine())!=null)
			{
				logger.info("==>"+line);
				if(line.contains("ROGER"))
					break;
			}
			
			is.close();
			os.close();
			
		} catch (Exception e) {
			logger.error("客户端Socket运行异常:"+e.getMessage(), e);
		}
		finally
		{
			if (socket != null) {    
                try {    
                	socket.close();  
                	logger.info("client socket closed");
                } catch (Exception e) {    
                	socket = null;
                	logger.error("客户端Socket关闭异常:"+e.getMessage(), e);  
                }    
            }  
		}

	}
}
