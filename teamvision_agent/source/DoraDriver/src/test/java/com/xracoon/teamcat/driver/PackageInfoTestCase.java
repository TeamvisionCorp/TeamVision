package com.xracoon.teamcat.driver;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.text.ParseException;

import javax.xml.parsers.ParserConfigurationException;

import org.junit.Test;
import org.xml.sax.SAXException;

import com.dd.plist.NSDictionary;
import com.dd.plist.PropertyListFormatException;
import com.dd.plist.PropertyListParser;
import com.xracoon.teamcat.utils.Zip;

public class PackageInfoTestCase {
	@Test 
	public void testUnzipOne() throws IOException{
		ByteArrayOutputStream baos=new ByteArrayOutputStream();
		Zip.unzip("C:/Users/Administrator/Desktop/ESports_Develop-iOS-ESports_rb37a9f3611.ipa","Payload/ESports.app/Info.plist", baos);
		System.out.println(baos.toString());
	}
	
	@Test
	public void testDdPlist() throws IOException, PropertyListFormatException, ParseException, ParserConfigurationException, SAXException{
		ByteArrayOutputStream baos=new ByteArrayOutputStream();
		Zip.unzip("C:/Users/Administrator/Desktop/ESports_Develop-iOS-ESports_rb37a9f3611.ipa", ".app/Info.plist", baos);
		NSDictionary dict= (NSDictionary) PropertyListParser.parse(baos.toByteArray());
		PropertyListParser.saveAsXML(dict, baos);
		System.out.println(dict.get("CFBundleName"));
		System.out.println(dict.get("CFBundleShortVersionString"));
		System.out.println(dict.get("CFBundleVersion"));
		System.out.println(dict.get("MinimumOSVersion"));
		System.out.println(dict.get("CFBundleIdentifier"));
		//CFBundleName, CFBundleShortVersionString, CFBundleVersion, MinimumOSVersion, CFBundleIdentifier
	}
	
	@Test
	public void testDBPlist1() throws IOException, PropertyListFormatException, ParseException, ParserConfigurationException, SAXException{
		ByteArrayOutputStream baos=new ByteArrayOutputStream();
		NSDictionary dict= (NSDictionary) PropertyListParser.parse(Files.readAllBytes(Paths.get("C:/Users/Administrator/Desktop/Info.plist")));
		PropertyListParser.saveAsXML(dict, baos);
		String str= baos.toString();
		System.out.println(dict.get("CFBundleName"));
		System.out.println(dict.get("CFBundleShortVersionString"));
		System.out.println(dict.get("CFBundleVersion"));
		System.out.println(dict.get("MinimumOSVersion"));
		System.out.println(dict.get("CFBundleIdentifier"));
	}
}
