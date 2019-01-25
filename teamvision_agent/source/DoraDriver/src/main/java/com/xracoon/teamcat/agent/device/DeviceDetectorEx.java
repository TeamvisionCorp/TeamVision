package com.xracoon.teamcat.agent.device;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.android.ddmlib.IDevice;
import com.xracoon.teamcat.agent.device.ddms.AndroidDeviceMonitor;
import com.xracoon.teamcat.agent.device.ddms.AndroidDeviceMonitor.IDeviceStateListener;
import com.xracoon.util.basekit.StringEx;
import com.xracoon.util.basekit.system.OS;

/**
 * 连接设备检测
 * @author Yangtianxin
 */
public class DeviceDetectorEx {
	private Logger logger = LoggerFactory.getLogger("DeviceDetectorEx");
	private boolean isMonitorStarted=false;
	
	private OS os;
	private Pattern psdk=Pattern.compile("ro\\.build\\.version\\.sdk=(.*?)(\\r\\n|$)");
	private Pattern prelease=Pattern.compile("ro\\.build\\.version\\.release=(.*?)(\\r\\n|$)");
	private Pattern pbrand= Pattern.compile("ro\\.product\\.brand=(.*?)(\\r\\n|$)");
	private Pattern pmodel=Pattern.compile("ro\\.product\\.model=(.*?)(\\r\\n|$)");
	private Pattern pproduct=Pattern.compile("ro\\.product\\.device=(.*?)(\\r\\n|$)"); //ro.build.product is obsolete, use ro.product.device
	
	private Pattern pdisplay=Pattern.compile("init=(\\d+)x(\\d+)\\s+(\\d+)dpi");
	//Frames: containing=[0,0][1080,1920] parent=[0,0][1080,1920] display=[0,0][1080,1920]
	public DeviceDetectorEx(OS os)
	{
		this.os=os;
	}
	public void setLogger(Logger logger)
	{
		this.logger=logger;
	}
	
	private AndroidDeviceMonitor  androidDevMonitor;
	private IDeviceStateListener innerListener;
	
	/**
	 * start device monitor,  WARNING: {@link #stopMonitor stopMonitor} method must be called when you will not detect device again 
	 */
	public synchronized void startMonitor()
	{
		androidDevMonitor=AndroidDeviceMonitor.getInstance();
		
		innerListener=new IDeviceStateListener(){
			@Override
			public void stateChange(String serialNo, IDevice rdev, boolean isOnline) {
				DeviceDetectorEx.this.stateChange(serialNo, rdev, isOnline);
			}};
		androidDevMonitor.addDeviceChangeListener(innerListener);
		
		androidDevMonitor.start();
		isMonitorStarted=true;
	}
	
	/**
	 * stop device monitor
	 */
	public synchronized void stopMonitor()
	{
		isMonitorStarted=false;
		androidDevMonitor.removeDeviceChangeListener(innerListener);
		androidDevMonitor.stop();
		androidDevs.clear();
	}
	
	private Map<String, DeviceAndroidEx> androidDevs=new LinkedHashMap<String, DeviceAndroidEx>();
	
	/**
	 * get online android devices,  {@link #startMonitor startMonitor} method must be called before this method,  {@link #stopMonitor stopMonitor} method must be called when you will not detect device again
	 * @return  Collections of {@link DeviceAndroidEx DeviceAndroidEx} represent online android device  
	 * @throws Exception   when {@link #startMonitor startMonitor} method not called before this method
	 */
	public Collection<DeviceAndroidEx> getOnlineDevices() throws Exception
	{
		if(!isMonitorStarted)
			throw new Exception("uninitialized, call startMonitor() first");
		
		List<DeviceAndroidEx> devices=new ArrayList<DeviceAndroidEx>();
		devices.addAll(androidDevs.values());
		return Collections.unmodifiableCollection(devices);
	}
	
	public DeviceAndroidEx getDevice(String serialNo)
	{
		return androidDevs.get(serialNo);
	}
	
	private void getAndroidDeviceDispalyInfo(DeviceAndroidEx dev)
	{
		String info=dev.synExec("dumpsys window displays"); //adb shell dumpsys window displays
		
		Matcher matcher= pdisplay.matcher(info);
		if(matcher.find())
		{
			int l1=Integer.parseInt(matcher.group(1));
			int l2=Integer.parseInt(matcher.group(2));
			dev.setResolution(l1>l2?(l1+"*"+l2):(l2+"*"+l1));
			dev.setDpi(matcher.group(3));
		}
		else
		{
			 info=dev.synExec("shell dumpsys window windows");
			 matcher= pdisplay.matcher(info);
			 if(matcher.find())
			 {
					int l1=Integer.parseInt(matcher.group(1));
					int l2=Integer.parseInt(matcher.group(2));
					dev.setResolution(l1>l2?(l1+"*"+l2):(l2+"*"+l1));
					dev.setDpi(matcher.group(3));
			 }
			else
			{
				dev.setResolution("unknown");
				dev.setDpi("unknown");
			}
		}
	}
	private void getAndroidDeviceDetail(DeviceAndroidEx dev)
	{
		String info=dev.synExec("cat /system/build.prop");
		Matcher matcher= psdk.matcher(info);
		if(matcher.find())
			dev.setSdk(Integer.parseInt(matcher.group(1)));
		
		matcher= prelease.matcher(info);
		if(matcher.find())
			dev.setOsVersion(matcher.group(1).trim().toLowerCase());

		//ro.product.brand | manufacturer
		matcher=pbrand.matcher(info);
		if(matcher.find())
			dev.setBrand(matcher.group(1).trim().toLowerCase());
	
		//ro.product.model | device | name
		matcher= pmodel.matcher(info);
		if(matcher.find())
		{
			String str=matcher.group(1).trim().toLowerCase();
			dev.setName(str);
		}
		//ro.product.model不存在则查找 ro.build.product
		else if(StringEx.isBlank(dev.getBrand()))
		{
			matcher= pproduct.matcher(info);
			if(matcher.find())
			{
				String str=matcher.group(1).trim().toLowerCase();
				dev.setName(str);
			}
			else
				dev.setName("unkown");
		}
		else
			dev.setName("unkown");
		
		boolean isSimu=dev.getName().equals("sdk") && dev.getSerialNo().startsWith("emulator-");
		dev.setIsSimulated(isSimu);
	}

	private void stateChange(String serialNo, IDevice rdev, boolean isOnline) {
		if(!androidDevs.containsKey(rdev.getSerialNumber()) && isOnline)
		{
			DeviceAndroidEx dev=new DeviceAndroidEx();
			dev.setDevRaw(rdev);
			dev.setSerialNo(serialNo);
			dev.setStatus("device");
			dev.setOS(os);
			
			getAndroidDeviceDetail(dev);
			getAndroidDeviceDispalyInfo(dev);
			androidDevs.put(serialNo, dev);
			
			logger.info("device online: "+serialNo);
		}
		else if(androidDevs.containsKey(serialNo) && !isOnline)
		{
			androidDevs.remove(serialNo);
			logger.info("device offline: "+serialNo);
		}
	}
	
	public static void main(String[] args) throws InterruptedException
	{
		DeviceDetectorEx dector=new DeviceDetectorEx(OS.getNewInstance());
		dector.startMonitor();
		Thread.sleep(10000);
		dector.stopMonitor();
	}
}
