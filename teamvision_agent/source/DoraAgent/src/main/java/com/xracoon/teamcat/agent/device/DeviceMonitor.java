package com.xracoon.teamcat.agent.device;

import java.io.File;
import java.util.Collection;
import java.util.Date;
import java.util.List;
import java.util.Map;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.xracoon.teamcat.agent.app.Agent;
import com.xracoon.teamcat.agent.device.Device;
import com.xracoon.teamcat.agent.device.DeviceAndroidEx;
import com.xracoon.teamcat.agent.device.DeviceDetectorEx;
import com.xracoon.teamcat.driver.DatasEnum;
import com.xracoon.util.basekit.system.OS;
import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

/**
 * 设备监测线程
 * 
 * @author Yangtianxin
 */
public class DeviceMonitor extends Thread {
	private Logger logger = LoggerFactory.getLogger("devMonLogger");
	private Agent agent;
	private OS os;
	private DeviceDetectorEx detector;
	private int agentID;
	private int scanInterval = 5000;

	public DeviceMonitor(Agent agent) {
		super(agent, "DevScanThread");
		this.os = agent.getOS().clone();
		os.setLogger(logger);
		this.agent = agent;
		this.agentID = agent.getAgentConfig().agentId;
		this.scanInterval = agent.getAgentConfig().devScanInterval;
	}
	
	public Device getDevice(String serialNo)
	{
		return detector==null?null:detector.getDevice(serialNo);
	}
	
	@Override
	public void run() {
		try {
			detector = new DeviceDetectorEx(os);
			detector.setLogger(logger);
			detector.startMonitor();
			
			logger.info("device monitor thread started");
			File lastDevFile = new File("lastDevScan");
			if (!lastDevFile.exists())
				lastDevFile.createNewFile();
			
			while (true) {
				try {
					Collection<DeviceAndroidEx> devices = detector.getOnlineDevices();
					
					
//					// 已经注册的设备
//					Map<String, Integer> registed = ds.getDeviceSerialNoOnAgent(agentID);
//					for (Device d : devices)
//					{
//						// 已经连接设备，已经注册，将设备offline状态置为online
//						List<AutotestingMobiledevice> d1 = ds.getDeviceBySerialNo(d.getSerialNo());
//						if (d1 != null && d1.size() == 1) 
//						{
//							if (d1.get(0).getMdeviceStatus() == DatasEnum.MobileDeviceStatus_Offline.getValue()) 
//							{
//								ds.updateMobileDeviceStatusByAgent(d.getSerialNo(), DatasEnum.MobileDeviceStatus_Online.getValue(), agentID);
//								logger.info("设备状态更新：" + d.getSerialNo() + "  online");
//							}
//
//							if (registed.containsKey(d.getSerialNo()))
//								registed.remove(d.getSerialNo());
//							
//						} else if (d1 != null && d1.size() == 0) // 已经连接设备，未注册
//						{
//							ds.addMobileDevice(d.getSerialNo(), d.getName(), d.getOsType(), d.getOsVersion(), d.getResolution(), agentID, true, d.isSimulated(), DatasEnum.MobileDeviceStatus_Online.getValue());
//							logger.info("注册新设备：" + d.getSerialNo() + "  online");
//						}
//					}
//					// 已经注册，未连接，将设备状态置为offline
//					for (String s : registed.keySet()) {
//						if (registed.get(s) != DatasEnum.MobileDeviceStatus_Offline.getValue()) {
//							ds.updateMobileDeviceStatusByAgent(s,
//									DatasEnum.MobileDeviceStatus_Offline.getValue(),
//									agentID);
//							logger.info("设备状态更新：" + s + "  offline");
//						}
//					}
				} catch (Exception e) {
					logger.error("Error in DevScan Loop: "+e.getMessage());
				}
				finally
				{
					lastDevFile.setLastModified(new Date().getTime());
					Thread.sleep(this.scanInterval);
				}
			}
		} catch (Exception e) {
			logger.error(e.getMessage(), e);
		}
		finally
		{
			detector.stopMonitor();
			detector=null;
		}
	}
	private JSONObject buildJson(Collection<DeviceAndroidEx> devices){
		JSONArray jsonDevs=new JSONArray();
		for(DeviceAndroidEx dev:devices){
			JSONObject jdev=new JSONObject();
			//ds.addMobileDevice(d.getSerialNo(), d.getName(), d.getOsType(), d.getOsVersion(), 
			//		d.getResolution(), agentID, true, d.isSimulated(), DatasEnum.MobileDeviceStatus_Online.getValue());
			jdev.put("serialNum", dev.getSerialNo());
			jdev.put("name", dev.getName());
			jdev.put("os", dev.getOsType());
			jdev.put("osVersion", dev.getOsVersion());
			jdev.put("screen", dev.getResolution());
			jdev.put("isSimulator", dev.isSimulated());
			jsonDevs.add(jdev);
		}
		
		JSONObject json=new JSONObject();
		json.put("agentId", agentID);
		json.put("devices", jsonDevs);
		
		return json;
	}
}
