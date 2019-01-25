package com.xracoon.teamcat.driver.step;

import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Iterator;
import java.util.List;

import com.xracoon.teamcat.driver.Driver;
import com.xracoon.teamcat.utils.AntFileUtil;
import com.xracoon.util.basekit.CollectionsEx;
import com.xracoon.util.basekit.FilesEx;
import com.xracoon.util.basekit.StringEx;
import com.xracoon.util.basekit.system.ExecStatus;
import com.xracoon.util.basekit.system.OS;

public class IOSPackageStep extends IOSBuildStep {
	private static String PN_CONF="-configuration";
	private static String PN_CERT="CODE_SIGN_IDENTITY";
	private static String PN_PROV="PROVISIONING_PROFILE_SPECIFIER";
	private static String PN_PROV_OLD="PROVISIONING_PROFILE";
	private static String PN_BUILDPATH="SYMROOT";
	private static String PN_CONFIGURATION_BUILD_DIR="CONFIGURATION_BUILD_DIR";
	
	private static int POD_NULL=19;
	private static int POD_INSTALL=17;
	private static int POD_BUILD=18;
	private static int POD_INSTALLBUILD=16;

	private void buildPods(File projPath, String podTypeString, boolean isClean,  String configuration, boolean isQuiet,  String buildPathPair) throws Exception{
		int podType=Integer.parseInt(podTypeString);
		if(podType==POD_NULL)
			return;
		
		if(podType==POD_INSTALL || podType==POD_INSTALLBUILD)
			OS.getSingleton().execSyn("pod install --no-repo-update", null, projPath);
		
		OS.getSingleton().execSyn("git diff Podfile.lock", null, projPath);
		
		File podPath=new File(projPath, "Pods");
		if(podType==POD_BUILD || podType==POD_INSTALLBUILD){
			List<String> opts=new ArrayList<>(Arrays.asList(new String[]{"xcodebuild","build","-alltargets"}));
			if(isClean)
				opts.add(1, "clean");
			if(!StringEx.isBlank(configuration)){
				opts.add(PN_CONF);
				opts.add(configuration);
			}
			if(isQuiet)
				opts.add("-quiet");
			opts.add(buildPathPair);
			ExecStatus ret= OS.getSingleton().execSyn(opts.toArray(new String[0]), null, podPath); 
			if(ret.getRetVal()!=0)
				throw new Exception("cocoapods build failed!");
		}
	}
	
	public int indexOfStart(Collection<? extends String> list, String prefix){
		if(list==null)
			return -1;
		
		@SuppressWarnings("unchecked")
		Iterator<String> iter=(Iterator<String>) list.iterator();
		int idx=0;
		while(iter.hasNext()){
			String v=iter.next();
			if(v==null && prefix==null || v!=null && v.startsWith(prefix))
				return idx;
			idx++;
		}
		return -1;
	}
	
	@Override
	public boolean exec() throws Exception {
		String xcode=stepConf.getParam("build_tool_xcode");
		String podType= stepConf.getParam("build_tool_pods");
		String cert=stepConf.getParam("ios_build_crendentials");
		String prov=stepConf.getParam("ios_build_provision");
		String extOptions=stepConf.getParam("ios_build_parameter","");
		String outputFilter=stepConf.getParam("ios_target_path");
		String projPath=stepConf.getParam("ios_project_dir");
		String is_clean_outputs=stepConf.getParam("is_clean_outputs");
		String is_upload_file=stepConf.getParam("is_upload_file");
		boolean result=true;
		if(is_clean_outputs !=null)
		{
			this.cleanOutput(outputFilter);	
		}

		
		boolean isClean=true;
		String configration="Release";
		File projectPath=new File(workspace, StringEx.isBlank(projPath)?".":projPath);
		File buildPath=new File(workspace, "build");
		
		//String target=stepConf.getParam("ios_build_target");
		
		//confirm xcode
		int xcodeVer=this.changeXCodeVersion(xcode);
		
		//options fix
		logger.info("-- ext options : "+extOptions);
		List<String> extOptionsList= StringEx.isBlank(extOptions)?new ArrayList<String>():StringEx.tokenize(extOptions);	
		int confIdx= CollectionsEx.indexOfIgnoreCase(extOptionsList, PN_CONF);
		if(confIdx>-1 && confIdx < extOptionsList.size()-1)
			configration=extOptionsList.get(confIdx+1);
		
		//..Cert
		if(!StringEx.isBlank(cert) &&
				indexOfStart(extOptionsList, PN_CERT)<0)
			extOptionsList.add( PN_CERT+"="+cert );
		//..Prov
		if(!StringEx.isBlank(prov) &&
				indexOfStart(extOptionsList, PN_PROV_OLD)<0)
			extOptionsList.add( (xcodeVer>=8?PN_PROV:PN_PROV_OLD)+"="+prov );
		//..BuidPath
		String buidPathParam= PN_BUILDPATH+"="+buildPath.getAbsolutePath();
		int buildPathIdx=indexOfStart(extOptionsList, PN_BUILDPATH);
		if(buildPathIdx<0)
			buildPathIdx=indexOfStart(extOptionsList, PN_CONFIGURATION_BUILD_DIR);
		
		if(buildPathIdx<0)
			extOptionsList.add(buidPathParam);
		else{
			buidPathParam=extOptionsList.get(buildPathIdx);
			String specbuildPath=buidPathParam.substring(buidPathParam.indexOf("=")+1).trim();
			if(!specbuildPath.startsWith(buildPath.getAbsolutePath()))
				buildPath=new File(this.workspace, specbuildPath);
			else
				buildPath=new File(specbuildPath);
		}
		
		boolean isQuiet=CollectionsEx.indexOfIgnoreCase(extOptionsList, "-quiet")>-1;
		logger.info("-- build path param : "+buidPathParam);
		String appSearchFilter=buidPathParam.contains(PN_CONFIGURATION_BUILD_DIR)?"*.app":configration+"*/*.app";
		logger.info("-- search app in path  : "+buildPath);
		logger.info("-- search app of filter: "+appSearchFilter);
		
		FilesEx.deleteContent(buildPath);
		
		//build..
		if(CollectionsEx.indexOfIgnoreCase(extOptionsList, "build")<0)
			extOptionsList.add(0, "build");
		//clean..
		if(isClean && CollectionsEx.indexOfIgnoreCase(extOptionsList, "clean")<0)
			extOptionsList.add(0, "clean");
		//xcodebuild..
		if(CollectionsEx.indexOfIgnoreCase(extOptionsList, "xcodebuild")<0)
			extOptionsList.add(0, "xcodebuild");
		
		
		//build pods
		buildPods(projectPath, podType, isClean, configration, isQuiet, buidPathParam);
		
		//build main project
		ExecStatus es= OS.getNewInstance()
				.execSyn(extOptionsList.toArray(new String[0]), null, projectPath);
		if(es.getRetVal()!=0)
			return false;
		
		//find .app
		File[] files=AntFileUtil.listAll(buildPath, appSearchFilter, null);
		if(files.length==0)
			throw new Exception("can't find '.app' output ");
		else if(files.length>1)
			throw new Exception("more than one '.app' output, can't distinguish "+Arrays.toString(files));
		
		//pack up
		File appFile=files[0];
		File ipaFile=new File(appFile.getParent(), appFile.getName().substring(0,appFile.getName().indexOf("."))+".ipa");
		String appfileString=appFile.getAbsolutePath();
		String ipaFileString=ipaFile.getAbsolutePath();
		
		String[] cmds=new String[]{"xcrun","-sdk", "iphoneos", "PackageApplication", "-v", appfileString, "-o", ipaFileString};
		es= OS.getNewInstance()
				.execSyn(cmds, null, projectPath);
		if(es.getRetVal()!=0)
			return false;
		
		//archive files
		 if(is_upload_file!=null)
	        {
	        	   result=this.archiveFiles(outputFilter, Driver.ARCHIVE_PACKAGE);
	        }
	        else
	        {
	        	    result=true;
	        }
		
		
		return result;
	}
}
