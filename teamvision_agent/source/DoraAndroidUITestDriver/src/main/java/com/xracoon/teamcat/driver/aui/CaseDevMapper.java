package com.xracoon.teamcat.driver.aui;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import com.xracoon.teamcat.agent.device.Device;
import com.xracoon.testutil.model.TestSuite;

@Deprecated
public class CaseDevMapper {

	private List<Device> filterDevices(Map<String,String> caseDevMaps, List<Device> allDev)
	{
		List<Device> useDevs=new ArrayList<Device>();
		Set<String> usedevIds=getSpecifiedDevices(caseDevMaps);
		for(Device dev: allDev)
		{
			if(usedevIds.contains(dev.getSerialNo()))
				useDevs.add(dev);
		}
		return useDevs;
	}
	
	private Map<String,String> gatherCasesForDev(TestSuite suite, String caseMap, String useDev)
	{
		Map<String,String> map=new HashMap<String,String>();
		String[] lines=caseMap.split("\n");
		for(String line:lines)
		{
			if(line.trim().length()>0 && line.contains("="))
			{
				String[] parts=line.split("=",2);
				String casePattern=parts[0].trim();
				String devPattern=parts[1].trim();
				map.put(casePattern,devPattern);
			}
		}
		return map;
	}
	
	private Set<String> getSpecifiedDevices(Map<String,String> caseDevMap)
	{
		Map<String,String> devices=new HashMap<String,String>();
		for(String str: caseDevMap.values())
			devices.put(str, str);
		return devices.keySet();
	}
}
