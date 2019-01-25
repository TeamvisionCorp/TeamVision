package com.xracoon.teamcat.agent.network;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Collection;
import java.util.Date;
import java.util.HashSet;
import java.util.Iterator;

import org.apache.log4j.Logger;

import com.xracoon.util.basekit.StringEx;
import redis.clients.jedis.JedisPubSub;

/**
 * redis消息队列处理类
 * @author Yangtianxin
 */
public class NetCmdExecutor extends JedisPubSub{
	private Logger logger = Logger.getLogger("netMonLogger");
	
	private Collection<INetCmdListener> listeners;
	public void addNetCmdListener(INetCmdListener listener) {
        if (listeners == null) {
            listeners = new HashSet<INetCmdListener>();
        }
        listeners.add(listener);
    }
	public void removeNetCmdListener(INetCmdListener listener) {
	        if (listeners == null)
	            return;
	        listeners.remove(listener);
	    }
	
	protected String fireStratEvent(NetCmd cmd) {
        Iterator<INetCmdListener> iter = listeners.iterator();
        StringBuilder builder=new StringBuilder();
        while (iter.hasNext()) {
        	INetCmdListener listener = iter.next();
        	String error=listener.startTask(cmd);
        	if(error!=null){
        		builder.append(error);
        		builder.append("\r\n");
        	}
        }
        return builder.toString();
	  }
	
	protected String fireStopEvent(NetCmd cmd) {
        Iterator<INetCmdListener> iter = listeners.iterator();
        StringBuilder builder=new StringBuilder();
        while (iter.hasNext()) {
        	INetCmdListener listener = iter.next();
        	String error=listener.stopTask(cmd);
        	if(error!=null){
        		builder.append(error);
        		builder.append("\r\n");
        	}
        }
        return builder.toString();
	  }
	
	protected boolean fireAliveEvent(NetCmd cmd) {
        Iterator<INetCmdListener> iter = listeners.iterator();
        boolean result=true;
        while (iter.hasNext()) {
        	INetCmdListener listener = iter.next();
        	result=result && listener.aliveTest(cmd);
        }
        return result;
	  }
	
	protected void fireShutdownEvent(NetCmd cmd) {
        Iterator<INetCmdListener> iter = listeners.iterator();
        while (iter.hasNext()) {
        	INetCmdListener listener = iter.next();
        	listener.stopAgent(cmd);
        }
	  }
	
	protected String fireTaskStateEvent(NetCmd cmd) {
        Iterator<INetCmdListener> iter = listeners.iterator();
        StringBuilder builder=new StringBuilder();
        while (iter.hasNext()) {
        	INetCmdListener listener = iter.next();
        	builder.append(listener.queryTaskState(cmd));
        	builder.append("\r\n");
        }
        return builder.toString();
	  }
	
	protected void fireRunErrorEvent(NetCmd cmd) {
        Iterator<INetCmdListener> iter = listeners.iterator();
        while (iter.hasNext()) {
        	INetCmdListener listener = iter.next();
        	listener.runError(cmd);
        }
	  }

	public NetCmdExecutor(){
	}

	@Override
	public void onMessage(String channel, String message) {
		//logger.info("handle cmd");
		try{
			File lastAliveFile=new File("lastAlive");
			if(!lastAliveFile.exists())
				lastAliveFile.createNewFile();

			String text=message.trim();
			if(text.equalsIgnoreCase(CmdMsg.Alive))
				lastAliveFile.setLastModified(new Date().getTime());
			else
				logger.info("server recive: "+text);
			
			NetCmd cmd=NetCmdParser.parseCmdLine(text);
			String error="";
			if(cmd==null){
				logger.error("received param is :"+text);
			}
			else if(cmd.type.equals(CmdMsg.Start)){
				error=this.fireStratEvent(cmd);
			}
			else if(cmd.type.equals(CmdMsg.Stop)){
				error=this.fireStopEvent(cmd);
			}
			else if(cmd.type.equals(CmdMsg.Timeout)){
				error=this.fireStopEvent(cmd);
			}
			else if(cmd.type.equals(CmdMsg.Alive)){
				logger.info(CmdMsg.AliveResponse+"\n");
			}
			else if(cmd.type.equals(CmdMsg.Shutdown)){
				this.fireShutdownEvent(cmd);
			}
			else if(cmd.type.equals(CmdMsg.TaskState)){
				error=this.fireTaskStateEvent(cmd);
			}
			else if(cmd.type.equals(CmdMsg.DRI_ErrorMsg)){
				this.fireRunErrorEvent(cmd);
			}
			else{
				logger.error("unknown msg received");
			}
			if(!StringEx.isBlank(error)){
				logger.error("error info :"+error);
			}else{
				logger.info("execute success");
			}
		}
		catch(Exception e) {
			logger.error("accept socket处理异常:" + e.getMessage(), e);
		}
	}
}
