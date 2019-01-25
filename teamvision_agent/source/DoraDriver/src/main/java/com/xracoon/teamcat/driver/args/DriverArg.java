package com.xracoon.teamcat.driver.args;

/**
 * Agent传递给Driver的数据项名字
 * @author Yangtianxin
 */
public class DriverArg {
	
	/**
	 * 自动化任务中针对Driver的额外配置，String类型
	 */
	public static final String DRIVERARG="driverArgs";
	
	/**
	 * 自动化任务中指定的用例id列表，Map<Integer,String>类型
	 */
	public static final String CASELIST="caseList";
	
	/**
	 * 自动化任务中指定使用的设备串号，String类型
	 */
	public static final String USEDEVICESN="useDev";
	
	/**
	 * 全局Wifi连接等待超时时间，int类型
	 */
	public static final String WIFITIMEOUT="wifiTimeout";
	
	/**
	 * 自动化任务中配置的Host映射，可用于检测环境是否正确。Map<String, String>类型
	 */
	public static final String HOSTMAP="host_map"; 
}
