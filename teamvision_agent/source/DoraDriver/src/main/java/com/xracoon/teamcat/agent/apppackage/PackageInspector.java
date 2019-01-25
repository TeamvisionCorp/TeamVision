package com.xracoon.teamcat.agent.apppackage;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;
import java.util.zip.ZipInputStream;

import com.xracoon.util.basekit.system.OS;

public class PackageInspector {
	private OS os;
	static final private Pattern patternPack=Pattern.compile("package: name='(\\S+)' ");
	static final private Pattern patternMainActivity=Pattern.compile("launchable-activity: name='(\\S+)' ");
	public PackageInspector(OS os)
	{
		this.os=os;
	}
	
	public ApkInfo getApkInfo(String apkPath)
	{
		ApkInfo apkInfo=new ApkInfo();
		String result=os.execSyn("aapt dump badging "+apkPath);
		Matcher matcher=patternPack.matcher(result);
		if(matcher.find())
			apkInfo.packIdentity=matcher.group(1);
		matcher=patternMainActivity.matcher(result);
		if(matcher.find())
			apkInfo.launcherActivity=matcher.group(1);
		
		return apkInfo;
	}
	/**
	 * extract file from apk
	 * @param apkPath
	 * @param fileInApk
	 * @param output   if output is not end with "/" or "\" ,it will be treated as a file  
	 * @throws IOException
	 */
	public void extractFileFromApk(String apkPath, String fileInApk, String output) throws IOException
	{
		ZipFile zf = new ZipFile(apkPath);  
        InputStream in = new BufferedInputStream(new FileInputStream(apkPath));  
        ZipInputStream zin = new ZipInputStream(in);  
        ZipEntry ze;  
        while ((ze = zin.getNextEntry()) != null) {  
            if (ze.isDirectory()) {
            } else {  
                long size = ze.getSize();  
                if (fileInApk.equalsIgnoreCase(ze.getName()))
                {  
                    BufferedReader br = new BufferedReader(new InputStreamReader(zf.getInputStream(ze)));  
                    if(output.endsWith("/")||output.endsWith("\\"))
                    	output+=ze.getName();
                    File file=new File(output);
                    if(!file.getParentFile().exists())
                    	file.getParentFile().mkdirs();
                    PrintWriter wr=new PrintWriter(new BufferedOutputStream(new FileOutputStream(output)));
                    String line;  
                    while ((line = br.readLine()) != null) {  
                       wr.println(line);
                    }  
                    br.close();  
                    wr.flush();
                    wr.close();
                }  
            }  
        }  
        zin.closeEntry(); 
	}
}
