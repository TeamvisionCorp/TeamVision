package com.xracoon.teamcat.driver;

import static org.junit.Assert.*;

import java.net.InetAddress;
import java.net.UnknownHostException;

import org.junit.Test;

import com.xracoon.util.basekit.system.OS;

public class OSTest {

	@Test
	public void test() {
		OS os=OS.getNewInstance();
		os.getIP("Intel|Realtek|TP-LINK|atheros");
	}

	@Test
	public void testHostResolve() throws UnknownHostException
	{
		System.out.println(InetAddress.getByName("user.laohu.com").getHostAddress());
	}
}
