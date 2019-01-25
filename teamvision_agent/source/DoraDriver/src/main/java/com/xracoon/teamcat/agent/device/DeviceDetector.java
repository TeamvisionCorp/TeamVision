package com.xracoon.teamcat.agent.device;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.commons.lang3.StringUtils;

import com.xracoon.util.basekit.system.OS;

/**
 * 连接设备检测
 * @author Yangtianxin
 */
@Deprecated
public class DeviceDetector {
	
	private OS os;
	private Pattern psdk=Pattern.compile("ro\\.build\\.version\\.sdk=(.*?)(\\r\\n|$)");
	private Pattern prelease=Pattern.compile("ro\\.build\\.version\\.release=(.*?)(\\r\\n|$)");
	private Pattern pbrand= Pattern.compile("ro\\.product\\.brand=(.*?)(\\r\\n|$)");
	private Pattern pmodel=Pattern.compile("ro\\.product\\.model=(.*?)(\\r\\n|$)");
	private Pattern pproduct=Pattern.compile("ro\\.product\\.device=(.*?)(\\r\\n|$)"); //ro.build.product is obsolete, use ro.product.device
	
	private Pattern pdisplay=Pattern.compile("init=(\\d+)x(\\d+)\\s+(\\d+)dpi");
	//Frames: containing=[0,0][1080,1920] parent=[0,0][1080,1920] display=[0,0][1080,1920]
	
	public DeviceDetector(OS os)
	{
		this.os=os;
	}
	
	public List<Device> detect()
	{
		List<Device> devices=new ArrayList<Device>();
		
		//Android
		List<DeviceAndroid> androidDevs=getAndroidDevices();
		for(Device d:androidDevs)
		{
			d.setOS(os);
			devices.add(d);
		}
		
		//Other Device
		//......
		
		return devices;
	}
	
	protected List<DeviceAndroid> getAndroidDevices()
	{
		ArrayList<DeviceAndroid> list=new ArrayList<DeviceAndroid>();
	
		String[] raw_infos=os.execSyn("adb devices").split("\r\n");
		ArrayList<String> infos=new ArrayList<String>();
		infos.addAll(Arrays.asList(raw_infos));

		while(infos.size()>0)
		{
			String line=infos.remove(0);
			if(line.trim().startsWith("List of devices"))
				break;
		}
		
		for(int i=0; i<infos.size(); i++)
		{
			String line=infos.get(i);
			if(line.trim().isEmpty())
				continue;
			
			String[] parts=line.split("\\s+");
			DeviceAndroid info =new DeviceAndroid();
			info.setSerialNo(parts[0].trim());
			info.setStatus(parts[1].trim());
			
			if(info.getStatus().equalsIgnoreCase("device"))
			{
				getAndroidDeviceDetail(info);
				getAndroidDeviceDispalyInfo(info);
			}
			list.add(info);
		}
		return list;
	}
	
	private void getAndroidDeviceDispalyInfo(DeviceAndroid devinfo)
	{
		String info=os.execSyn("adb -s "+devinfo.getSerialNo()+" shell dumpsys window displays"); //adb shell dumpsys window displays
		
		Matcher matcher= pdisplay.matcher(info);
		if(matcher.find())
		{
			int l1=Integer.parseInt(matcher.group(1));
			int l2=Integer.parseInt(matcher.group(2));
			devinfo.setResolution(l1>l2?(l1+"*"+l2):(l2+"*"+l1));
			devinfo.setDpi(matcher.group(3));
		}
		else
		{
			 info=os.execSyn("adb -s "+devinfo.getSerialNo()+" shell dumpsys window windows");
			 matcher= pdisplay.matcher(info);
			 if(matcher.find())
			 {
					int l1=Integer.parseInt(matcher.group(1));
					int l2=Integer.parseInt(matcher.group(2));
					devinfo.setResolution(l1>l2?(l1+"*"+l2):(l2+"*"+l1));
					devinfo.setDpi(matcher.group(3));
			 }
			else
			{
				devinfo.setResolution("unknown");
				devinfo.setDpi("unknown");
			}
		}
	}
	private void getAndroidDeviceDetail(DeviceAndroid devinfo)
	{
		String info=os.execSyn("adb -s "+devinfo.getSerialNo()+" shell cat /system/build.prop");
		Matcher matcher= psdk.matcher(info);
		if(matcher.find())
			devinfo.setSdk(Integer.parseInt(matcher.group(1)));
		
		matcher= prelease.matcher(info);
		if(matcher.find())
			devinfo.setOsVersion(matcher.group(1).trim().toLowerCase());

		//ro.product.brand | manufacturer
		matcher=pbrand.matcher(info);
		if(matcher.find())
			devinfo.setBrand(matcher.group(1).trim().toLowerCase());
	
		//ro.product.model | device | name
		matcher= pmodel.matcher(info);
		if(matcher.find())
		{
			String str=matcher.group(1).trim().toLowerCase();
			devinfo.setName(str);
		}
		//ro.product.model不存在则查找 ro.build.product
		else if(StringUtils.isBlank(devinfo.getBrand()))
		{
			matcher= pproduct.matcher(info);
			if(matcher.find())
			{
				String str=matcher.group(1).trim().toLowerCase();
				devinfo.setName(str);
			}
			else
				devinfo.setName("unkown");
		}
		else
			devinfo.setName("unkown");
		
		boolean isSimu=devinfo.getName().equals("sdk") && devinfo.getSerialNo().startsWith("emulator-");
		devinfo.setIsSimulated(isSimu);
	}
}
