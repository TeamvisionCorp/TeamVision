package com.xracoon.teamcat.agent.network;

import java.util.EventListener;

/**
 * 网络命令监听器
 * @author Yangtianxin
 */
public interface INetCmdListener extends EventListener {
	String startTask(NetCmd cmd);
	String stopTask(NetCmd cmd);
	boolean aliveTest(NetCmd cmd);
	boolean stopAgent(NetCmd cmd);
	
	String queryTaskState(NetCmd cmd);
	void runError(NetCmd cmd);
}