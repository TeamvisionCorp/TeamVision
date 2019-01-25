package com.xracoon.teamcat.agent.network;

public class CmdMsg {
	public static final String Start="START";
	public static final String Stop="STOP";
	public static final String Timeout="TIMEOUT";
	
	public static final String Alive="ALIVE";
	public static final String Shutdown="SHUTDOWN";
	public static final String TaskState="TASKSTATE";
	
	public static final String AliveResponse="alive";
	public static final String UnknownCmd="CMD_FORMAT_ERROR";
	public static final String ExecFail="FAIL";
	
	public static final String DRI_ErrorMsg="RUNERROR";
}
