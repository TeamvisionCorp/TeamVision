package com.xracoon.teamcat.driver;

import java.io.IOException;
import java.util.List;

import org.junit.Test;
import static org.junit.Assert.*;

import com.xracoon.teamcat.agent.apppackage.ApkInfo;
import com.xracoon.teamcat.agent.apppackage.PackageInspector;
import com.xracoon.teamcat.agent.device.Device;
import com.xracoon.teamcat.agent.device.DeviceDetector;
import com.xracoon.util.basekit.system.OS;

public class AndroidDeviceTest {

	@Test
	public void testInstall() {
		OS os=OS.getNewInstance();
		List<Device> devices=new DeviceDetector(os).detect();
		String testPackage="D:/agent/workdir/UITest_LaohuSDK_3.6-release.apk";
		String appPackage="D:/agent/workdir/LaohuSDK_Demo-formal-proguard-3.7.3-r53907_debug.apk";
		for(Device dev: devices)
		{
			System.out.println("install "+testPackage+": "+dev.installApp(testPackage));
			System.out.println("install "+appPackage+": "+dev.installApp(appPackage));
		}
	}

	@Test
	public void testGetApkInfo() {
		OS os=OS.getNewInstance();
		String testPackage="D:/agent/workdir/UITest_LaohuSDK_3.6-release.apk";
		String appPackage="D:/agent/workdir/LaohuSDK_Demo-formal-proguard-3.7.3-r53907_debug.apk";
		
		PackageInspector apkInspector=new PackageInspector(os);
		ApkInfo testApkInfo=apkInspector.getApkInfo(testPackage);
		ApkInfo appInfo=apkInspector.getApkInfo(appPackage);
	}
	
	@Test
	public void testExtractFileFromApk() throws IOException {
		OS os=OS.getNewInstance();
		String testPackage="D:/agent/workdir/UITest_LaohuSDK_3.6-release.apk";
		String appPackage="D:/agent/workdir/LaohuSDK_Demo-formal-proguard-3.7.3-r53907_debug.apk";
		
		PackageInspector apkInspector=new PackageInspector(os);
		apkInspector.extractFileFromApk(testPackage, "assets/testsuite.xml", "D:/agent/workdir/testsuite.xml");
	}
}
