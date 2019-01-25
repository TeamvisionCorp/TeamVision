package com.xracoon.teamcat.agent.debug;
import static org.junit.Assert.*;

import java.net.UnknownHostException;
import java.util.HashMap;

import org.junit.Test;

import com.xracoon.util.basekit.system.OS;


public class OSTest {

	@Test
	public void testUpdateHost() throws Exception 
	{
		OS os=OS.getNewInstance();
		HashMap<String,String> maps=new HashMap<String,String>();
		
		String ip1="111.111.111.111";
		String hostname1="ostest1.com";
		String ip2="121.121.121.121";
		String hostname2="ostest2.com";
		maps.put(hostname1, ip1);
		maps.put(hostname2, ip2);
		os.updateHost(maps);
		
		assertTrue(os.getIPByHost(hostname1).equals(ip1));
		assertTrue(os.getIPByHost(hostname2).equals(ip2));
	}
	
	
	@Test
	public void testGetIP() throws UnknownHostException
	{
		OS os=OS.getNewInstance();
		System.out.println(os.getLocalIP());
	}
	
	@Test
	public void testRemoveHost() throws Exception 
	{
		OS os=OS.getNewInstance();
		HashMap<String,String> maps=new HashMap<String,String>();
		
		String ip1="";
		String hostname1="ostest3.com";

		maps.put(hostname1, ip1);
		os.updateHost(maps);
		
		//assertTrue(os.getHostIP(hostname1).equals(ip1));
	}
}
