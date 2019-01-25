package com.xracoon.teamcat.driver.step;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.xml.parsers.ParserConfigurationException;
import org.xml.sax.SAXException;
import com.dd.plist.NSDictionary;
import com.dd.plist.PropertyListFormatException;
import com.dd.plist.PropertyListParser;
import com.xracoon.teamcat.utils.Zip;
import com.xracoon.util.basekit.StringEx;


public class XcodeSettingsCheckStep extends BuildStep {

	@Override
	public boolean exec() throws Exception {
		List<String> errorList=new ArrayList<String>();
		String outputFilter = stepConf.getParam("ipafileFilter");
		HashMap<String, String> expectResult =getExpectResult();
		HashMap<String, String> actualResult = new HashMap<String, String>();
		actualResult.putAll(expectResult);
		File ipaFile=getIpaFile(outputFilter);
		actualResult =getValueFromInfoPlist(ipaFile,actualResult);
		errorList=checkFieldValue(expectResult, actualResult);
		if(errorList.size()>0)
		{
			logger.info("-----------------Output error message for check result.------------");
			for(String errorMessage:errorList)
			{
				logger.info(errorMessage);
			}
			return false;
		}
		else
		{
			logger.info("Check result is pass");
		}
		return true;
	}
	
	private List<String> checkFieldValue(HashMap<String,String> expectResult,HashMap<String,String> actualResult)
	{
		List<String> errorList=new ArrayList<String>();
		logger.info("-------------------Start to check xcode settings--------------");
		for (Map.Entry<String, String> entry : expectResult.entrySet()) {
			if (!entry.getValue().trim().equals("{SKIP}")) {
				logger.info("Settings field is: " + entry.getKey());
				logger.info("Expected value is: " + entry.getValue());
				logger.info(" Actual value is: " + actualResult.get(entry.getKey()).toString());
				if(entry.getKey().equals("CFBundleVersion"))
				{
					if(entry.getValue().trim().equals(""))
					{
						Long actual_bound_version=Long.parseLong(actualResult.get(entry.getKey()).toString())*1000;
						Long current_time_stmap=System.currentTimeMillis();
						int timeDiff=(int)(current_time_stmap-actual_bound_version);
						if(timeDiff<0||timeDiff>10*60*1000)
						{
							String errorMessage="Settings field "+entry.getKey()+" check fail";
							errorMessage=errorMessage+"! the default time diff is 10 min";
							errorList.add(errorMessage);
						}
					    logger.info("CFBundleVersion time diff is "+String.valueOf(timeDiff)+"mils");
					}
				}
				else if(!entry.getValue().equals(actualResult.get(entry.getKey()).toString()))
				{
					String errorMessage="Settings field "+entry.getKey()+" check fail";
					errorList.add(errorMessage);
				}
			} 
			else 
			{
				logger.info("----------------------------------------------");
				logger.info("Settings filed is: " + entry.getKey() + " and skip checking!");
			}
		}
		return errorList;
	}

	private File getIpaFile(String outputFilter) throws Exception {
		if (StringEx.isBlank(outputFilter)) {
			throw new Exception("未指定产出文件");
		}
		File first_file = null;
		File[] files = listOutputFilterFile(outputFilter);

		// get first ipa file
		for (int i = 0, len = files.length; i < len; i++) {
			File f = files[i];
			if (f.getName().toLowerCase().endsWith(".ipa")) {
				first_file = f;
			}
			if (f.getName().toLowerCase().endsWith(".apk")) {
				break;
			}
		}
		return first_file;

		
	}
	
	private HashMap<String,String> getValueFromInfoPlist(File f,HashMap<String,String> keyValuePairs ) throws IOException, PropertyListFormatException, ParseException, ParserConfigurationException, SAXException
	{
		ByteArrayOutputStream baos = new ByteArrayOutputStream();
		Zip.unzip(f.getAbsolutePath(), ".app/Info.plist", baos);
		NSDictionary dict = (NSDictionary) PropertyListParser.parse(baos.toByteArray());
		PropertyListParser.saveAsXML(dict, baos);
		for (Map.Entry<String, String> entry : keyValuePairs.entrySet()) {
			if(dict.containsKey(entry.getKey()))
			{
				String temp = dict.get(entry.getKey()).toString();
				entry.setValue(temp);
			}
			else
			{
				entry.setValue("Field "+entry.getKey()+" doesn't exist in info.plist !");
			}
			
		}
		return keyValuePairs;
	}
    
	private HashMap<String,String> getExpectResult()
	{
		String CFBundleIdentifier = stepConf.getParam("CFBundleIdentifier");
		String CFBundleShortVersionString = stepConf.getParam("CFBundleShortVersionString");
		String CFBundleVersion = stepConf.getParam("CFBundleVersion");
		String MinimumOSVersion = stepConf.getParam("MinimumOSVersion");
		HashMap<String, String> expectResult = new HashMap<String, String>();
		expectResult.put("CFBundleIdentifier", CFBundleIdentifier);
		expectResult.put("CFBundleShortVersionString", CFBundleShortVersionString);
		expectResult.put("CFBundleVersion",CFBundleVersion);
		expectResult.put("MinimumOSVersion",MinimumOSVersion);
		return expectResult;
	}
}
