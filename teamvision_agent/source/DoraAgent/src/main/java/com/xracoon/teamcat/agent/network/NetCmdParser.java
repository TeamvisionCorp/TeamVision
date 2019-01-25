package com.xracoon.teamcat.agent.network;

import java.util.HashMap;
import org.apache.log4j.Logger;
import net.sf.json.JSONObject;

/**
 * Socket网络命令解析类
 * @author Yangtianxin
 */
public class NetCmdParser {
	static private Logger logger = Logger.getLogger(NetCmdExecutor.class);
	
	static public NetCmd parseCmdLine(String cmdline){
		try{
			NetCmd cmd=new NetCmd();
			
			//先按Json解析
			if(cmdline.matches("\\s*\\{.+:.+\\}\\s*")){
				JSONObject json=JSONObject.fromObject(cmdline);
				cmd.type=json.getString("cmd").toUpperCase();
				cmd.args=new HashMap<>();
				for(Object k:json.keySet())
					cmd.args.put(k.toString(), json.getString(k.toString()));
				if(cmd.args.containsKey("taskQueueId"))
					cmd.tqID=Integer.parseInt(cmd.args.get("taskQueueId"));
			}
			else{
				String[] parts=cmdline.toUpperCase().split("\\s");
				cmd.type=parts[0];
				if(cmd.type.equals(CmdMsg.Start) || cmd.type.equals(CmdMsg.Stop) || cmd.type.equals(CmdMsg.Timeout))
					cmd.tqID=Integer.parseInt(parts[1]);
				
				if(cmd.type.equals(CmdMsg.Stop))
					cmd.desc="abort";
				else if(cmd.type.equals(CmdMsg.Timeout))
					cmd.desc="timeout";
			}
			return cmd;
		}catch(Exception e)
		{
			logger.error("网络命令解析错误:"+e.getMessage(),e);
			return null;
		}
	}
	static public String toCmdLine(NetCmd cmd)
	{
		return null;
	}
}
