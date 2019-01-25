package com.xracoon.teamcat.driver;

import java.io.PrintWriter;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.xracoon.teamcat.agent.device.Device;
import com.xracoon.teamcat.agent.device.DeviceAndroidEx;
import com.xracoon.teamcat.agent.device.DeviceDetectorEx;
import com.xracoon.teamcat.agent.device.EndingLineListener;
import com.xracoon.teamcat.agent.device.Execution;
import com.xracoon.util.basekit.system.OS;

public class AndroidDeviceExTest {
	private static Logger logger = LoggerFactory.getLogger(AndroidDeviceExTest.class);
	private Device dev;
	private DeviceDetectorEx detector;
	
	@Before
	public void setUp() throws Exception
	{
		OS os=OS.getNewInstance();
		detector = new DeviceDetectorEx(os);
		detector.setLogger(logger);
		detector.startMonitor();
		
		System.out.println("waiting for device...");
		while(dev==null)
		{
			Thread.sleep(500);
			dev=detector.getOnlineDevices().iterator().next();
		}
		System.out.println("get device "+dev.getSerialNo());
	}
	
	@After
	public void tearDown()
	{
		detector.stopMonitor();
	}
	
	@Test
	public void testListDevices() throws Exception 
	{
		for(DeviceAndroidEx dev: detector.getOnlineDevices())
		{
			System.out.println(dev.getSerialNo());
		}
	}

	@Test
	public void testSynExec() throws Exception
	{
		System.out.println("==>before remoteExec");
		String out=dev.synExec("am broadcast -a com.xracoon.wifisetter.CONFIG_BROADCAST --es ssid Txtest --es pw qwert12345");
		System.out.println(out);
		System.out.println("==>after remoteExec");
	}
	

	@Test
	public void testAsynExecNormalEnd() throws Exception
	{
		System.out.println("==>before remoteExec");
		
		Execution execution=dev.asynExec("ls",new PrintWriter(System.out), null);
		execution.waitFor();
		
		System.out.println("==>after remoteExec");
	}
	
	@Test
	public void testAsynExecEndListener() throws Exception
	{
		System.out.println("==>before remoteExec");
		
		Execution execution=dev.asynExec("logcat",new PrintWriter(System.out), new EndingLineListener(){
			@Override
			public boolean isEnding(String line) {
				return line.contains("bye!");
			}});
		execution.waitFor();
		
		System.out.println("==>after remoteExec");
		System.out.println("---------output----------");
		System.out.println(execution.getOutput());
	}
	
	@Test
	public void testAsynExecWhitoutWriter() throws Exception
	{
		System.out.println("==>before remoteExec");
		
		Execution execution=dev.asynExec("logcat",null, new EndingLineListener(){
			@Override
			public boolean isEnding(String line) {
				return line.contains("bye!");
			}});
		execution.waitFor();
		System.out.println("==>after remoteExec");
		System.out.println("---------output----------");
		System.out.println(execution.getOutput());
	}
	
	@Test
	public void testAsynExecStop() throws Exception
	{
		System.out.println("==>before remoteExec");
		
		Execution execution=dev.asynExec("logcat",new PrintWriter(System.out), null);
		Thread.sleep(3000);
			execution.stop();
		
		System.out.println("==>after remoteExec");
	}
	
	@Test
	public void testCaptureLogcat() throws Exception
	{
		System.out.println("==>before remoteExec");
		DeviceAndroidEx adev=(DeviceAndroidEx)dev;
		Execution execution=adev.captureLog("dalvikvm:D", true, null);
		Thread.sleep(5000);
			execution.stop();
		
		System.out.println("==>after remoteExec");
		System.out.println("---------output----------");
		System.out.println(execution.getOutput());
	}
	
	@Test
	public void testCaptureLogcatWithWirter() throws Exception
	{
		System.out.println("==>before remoteExec");
		DeviceAndroidEx adev=(DeviceAndroidEx)dev;
		Execution execution=adev.captureLog("dalvikvm:D", true, new PrintWriter(System.out));
		Thread.sleep(5000);
			execution.stop();
		
		System.out.println("==>after remoteExec");
		System.out.println("---------output----------");
		System.out.println(execution.getOutput());
	}
}
